import asyncio
import logging
import os
from itertools import count
from typing import Any, Dict, cast

import fastapi
from transformers import PreTrainedTokenizerFast

from briton.briton import BritonInteractor, BritonInteractorImpl
from briton.checks import trllm_config_check
from briton.constants import (
    DEFAULT_BRITON_PORT,
    DEFAULT_MAX_FSM_WORKERS,
    OPENAI_COMPATIBLE_TAG,
    TOOL_CALL_IDS,
    TOOL_CALL_TOKENS,
)
from briton.error_handling import grpc_error_handling
from briton.fsm_cache import FsmCache, add_schema_to_cache
from briton.input_utils import set_briton_request_fields_from_model_input
from briton.openai import create_completion, create_completion_chunks
from briton.proto import InferenceRequest
from briton.schema import get_prompt, update_raw_model_input, validate_model_input
from briton.secrets import get_hf_token_or_none
from briton.trtllm_build_config import (
    TrussTRTLLMBatchSchedulerPolicy,
    TrussTRTLLMBuildConfiguration,
)
from briton.truss_monitor import start_monitor


logger = logging.getLogger(__name__)


class Model:
    def __init__(self, **kwargs):
        self._loaded = False
        self._model = None
        self._config = kwargs["config"]
        self._data_dir = kwargs["data_dir"]
        self._secrets = kwargs["secrets"]
        self._request_id_counter = count(start=1)
        self._briton_process = None
        model_metadata = self._config.get("model_metadata", {})
        tags = model_metadata.get("tags", [])
        self._uses_openai_api = OPENAI_COMPATIBLE_TAG in tags
        trllm_config_check(self._config)
        trtllm_config = self._config.get("trt_llm")
        truss_trtllm_build_config = TrussTRTLLMBuildConfiguration(**trtllm_config.get("build"))
        self._base_model = truss_trtllm_build_config.base_model
        self._tp_count = truss_trtllm_build_config.tensor_parallel_count
        self._tokenizer_repository = truss_trtllm_build_config.checkpoint_repository.repo
        self._kv_cache_free_gpu_mem_fraction = (
            truss_trtllm_build_config.kv_cache_free_gpu_mem_fraction
        )
        self._enable_kv_cache_reuse = (
            truss_trtllm_build_config.plugin_configuration.use_paged_context_fmha
        )
        self._enable_chunked_context = truss_trtllm_build_config.enable_chunked_context
        self._max_num_tokens = truss_trtllm_build_config.max_num_tokens
        self._max_seq_len = truss_trtllm_build_config.max_seq_len
        self._batch_scheduler_policy = _batch_scheduler_policy_to_int(
            truss_trtllm_build_config.batch_scheduler_policy
        )
        self._default_max_tokens = truss_trtllm_build_config.default_max_tokens
        self._hf_token = get_hf_token_or_none(self._secrets)
        self._lazy_init_done = False
        self._lazy_init_lock = None
        self._stub = None
        self._max_fsm_workers = DEFAULT_MAX_FSM_WORKERS

        # Allow passing briton_interactor for ease of testing
        self._briton_interactor: BritonInteractor = model_metadata.get(
            "briton_interactor", BritonInteractorImpl()
        )
        self._tool_call_token = TOOL_CALL_TOKENS.get(self._base_model)
        self._tool_call_token_id = TOOL_CALL_IDS.get(self._base_model)

    def load(self):
        if self._loaded:
            return

        # TODO(pankaj) Support loading bundled tokenizer rather than from HF
        self._tokenizer = cast(
            PreTrainedTokenizerFast,
            self._briton_interactor.auto_tokenizer_from_pretrained(
                self._tokenizer_repository, hf_token=self._hf_token
            ),
        )

        # We only support Llama and mistral with Briton, for which this should
        # apply.
        assert isinstance(self._tokenizer, PreTrainedTokenizerFast)

        # These are tokens outside of tokenizer.json. We need to pass these to
        # Briton, to pass to rust tokenizer.
        added_token_decoders = self._tokenizer.added_tokens_decoder
        added_tokens = [token for token in added_token_decoders.values()]

        self._check_supports_tool_calls()

        self._fsm_cache = FsmCache(
            self._briton_interactor.fsm_cache_dir(),
            self._tokenizer,
            self._max_fsm_workers,
            self._tool_call_token_id,
        )

        load_briton = self._briton_interactor.load
        load_briton(
            model_name="briton",
            engine_path=self._data_dir,
            hf_tokenizer=self._tokenizer_repository,
            work_dir=self._data_dir,
            fsm_cache_dir=self._fsm_cache.cache_dir,
            kv_cache_free_gpu_mem_fraction=self._kv_cache_free_gpu_mem_fraction,
            port=DEFAULT_BRITON_PORT,
            added_tokens=added_tokens,
            max_num_tokens=self._max_num_tokens,
            enable_chunked_context=self._enable_chunked_context,
            hf_token=self._hf_token,
            tp_count=self._tp_count,
            batch_scheduler_policy=self._batch_scheduler_policy,
        )
        self._loaded = True

    async def predict(self, model_input: Dict[str, Any], request: fastapi.Request):
        """
        Run inference

        Note that the async nature of this function is a little tricky. Care is
        needed to make sure this function is a regular async function and not an
        async generator, i.e. there shouldn't be any direct yields in this
        function. This is because we need to support both streaming and
        non-streaming cases in this function. We do this by either returning an
        async-generator for the streaming case, or directly the full text for
        the other case. Returning an async generator for non-streaming case
        interferes with the open ai client proxy.
        """

        # TODO(pankaj) Wire up request cancellation
        async def is_cancelled_fn():
            disconnected = await request.is_disconnected()
            if disconnected:
                logger.info("Request disconnected, cancelling.")
            return disconnected

        if not self._lazy_init_done:
            # While this isn't completely safe, the async lock needs to be
            # created within the same async loop where it will be used. Ideally,
            # the proper solution would involve supporting asynchronous load
            # function, but that is not currently supported in Truss. The risk is
            # that multiple initial requests could end up with different lock
            # instances, making the lock ineffective. In practice, this is
            # highly unlikely. This issue could occur if one request executes
            # the line below and then gets preempted, allowing another request
            # to execute the same line. However, since there is no async
            # operation in the following line, it is very unlikely for the
            # request to be preempted at that point.
            if self._lazy_init_lock is None:
                self._lazy_init_lock = asyncio.Lock()

            async with self._lazy_init_lock:
                self._stub = self._briton_interactor.create_grpc_stub(DEFAULT_BRITON_PORT)
                await start_monitor(self._briton_interactor, logger)
                self._lazy_init_done = True

        validated_input = validate_model_input(
            model_input=model_input, supports_tools=self._tool_call_token is not None
        )
        prompt = get_prompt(validated_input, self._tokenizer)
        model_input.pop("messages", None)
        input_ids = self._tokenizer.encode(prompt, add_special_tokens=False)
        prompt_tokens = len(input_ids)

        request_id = self._calc_request_id()
        briton_request = InferenceRequest(
            request_id=request_id,
            input_text=prompt,
        )
        self._update_request_end_id_pad_id(briton_request, model_input)

        schema = validated_input.output_json_schema
        if schema is not None:
            briton_request.output_schema_hash = await add_schema_to_cache(self._fsm_cache, schema)
            force_tools = validated_input.force_tools
            if force_tools is not None:
                briton_request.force_tools = force_tools

        update_raw_model_input(model_input, validated_input)
        if "max_tokens" not in model_input and self._default_max_tokens is not None:
            model_max_allowed_tokens = self._max_seq_len - prompt_tokens
            model_input["max_tokens"] = min(model_max_allowed_tokens, self._default_max_tokens)

        set_briton_request_fields_from_model_input(model_input, briton_request)
        for words in ["bad_words", "stop_words"]:
            if words in model_input:
                for word in model_input[words].split(","):
                    getattr(briton_request, words).append(word)

        resp_iter = self._stub.Infer(briton_request)

        # Get model name for openai compatibility
        model_name = validated_input.model if validated_input.model else ""

        # Default for OpenAI API is to not stream, but old Briton default was to stream.
        stream_predicate = (self._uses_openai_api and validated_input.stream) or (
            not self._uses_openai_api and model_input.get("stream", True)
        )

        with grpc_error_handling():
            if stream_predicate:
                completion_tokens = 0

                # Advance the iterator to get the first chunk, to allow any validation error to be thrown
                async for first_chunk in resp_iter:
                    break

                async def generate_after_first_chunk():
                    nonlocal completion_tokens
                    completion_tokens += len(first_chunk.output_ids)
                    yield first_chunk.output_text
                    async for chunk in resp_iter:
                        completion_tokens += len(chunk.output_ids)
                        yield chunk.output_text

                def completion_tokens_fn():
                    nonlocal completion_tokens
                    return completion_tokens

                async def generate_processed_after_first_chunk():
                    output_text = first_chunk.output_text
                    # Try to remove tool call token from first chunk only
                    if self._tool_call_token is not None:
                        output_text = output_text.removeprefix(self._tool_call_token)
                    eos_token = self._eos_token()
                    if eos_token is not None:
                        output_text = output_text.removesuffix(eos_token)
                    yield output_text

                    async for chunk in resp_iter:
                        output_text = chunk.output_text
                        if eos_token is not None:
                            output_text = output_text.removesuffix(eos_token)
                        yield output_text

                if self._uses_openai_api:
                    return create_completion_chunks(
                        req_id=str(request_id),
                        model=model_name,
                        input_text=generate_after_first_chunk(),
                        eos_token=self._eos_token(),
                        tool_token=self._tool_call_token,
                        prompt_tokens=(
                            prompt_tokens if validated_input.include_stream_usage else None
                        ),
                        completion_tokens_fn=(
                            completion_tokens_fn if validated_input.include_stream_usage else None
                        ),
                    )
                else:
                    return generate_processed_after_first_chunk()
            else:
                full_text, completion_tokens = await _collect_text(resp_iter)
                if self._uses_openai_api:
                    return create_completion(
                        req_id=str(request_id),
                        model=model_name,
                        input_text=full_text,
                        eos_token=self._eos_token(),
                        tool_token=self._tool_call_token,
                        prompt_tokens=prompt_tokens,
                        completion_tokens=completion_tokens,
                    )
                else:
                    eos_token = self._eos_token()
                    if eos_token is not None:
                        full_text = full_text.removesuffix(eos_token)
                    if self._tool_call_token is not None:
                        full_text = full_text.removeprefix(self._tool_call_token)
                    return full_text

    def _calc_request_id(self) -> int:
        """Calculate unique request id.

        Not thread safe, but safe to use in single threaded async context. There
        are no async operations here, so this function is unlikely to be
        preempted in the middle. This is important otherwise we may end up with
        duplicate ids.
        """
        return int(str(os.getpid()) + str(next(self._request_id_counter)))

    def _eos_token(self):
        return getattr(self._tokenizer, "eos_token", None)

    def _eos_token_id(self):
        return getattr(self._tokenizer, "eos_token_id", None)

    def _pad_token_id(self):
        return getattr(self._tokenizer, "pad_token_id", None)

    def _update_request_end_id_pad_id(self, request, model_input):
        end_id = model_input.get("end_id", None) or self._eos_token_id()
        if end_id is not None:
            request.end_id = end_id
        pad_id = model_input.get("pad_id", None) or self._pad_token_id()
        if pad_id is not None:
            request.pad_id = pad_id

    def _check_supports_tool_calls(self):
        if (
            self._tool_call_token is None
            or self._tokenizer.convert_tokens_to_ids(self._tool_call_token)
            == self._tokenizer.unk_token_id
        ):
            self._tool_call_token = None
            self._tool_call_token_id = None


async def _collect_text(async_text_iter) -> tuple[str, int]:
    full_text = ""
    completion_tokens = 0
    async for delta in async_text_iter:
        completion_tokens += len(delta.output_ids)
        full_text += delta.output_text
    return full_text, completion_tokens


def _batch_scheduler_policy_to_int(policy: TrussTRTLLMBatchSchedulerPolicy) -> int:
    if policy == TrussTRTLLMBatchSchedulerPolicy.MAX_UTILIZATION:
        return 0
    elif policy == TrussTRTLLMBatchSchedulerPolicy.GUARANTEED_NO_EVICT:
        return 1
    else:
        logger.warning(f"Unknown batch scheduler policy: {policy}. Using GUARANTEED_NO_EVICT.")
        return 1
