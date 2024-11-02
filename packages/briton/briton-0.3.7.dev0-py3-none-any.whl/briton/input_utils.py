from typing import Any, Dict

from fastapi import HTTPException

from briton.constants import MODEL_INPUT_TO_BRITON_FIELD
from briton.proto import InferenceRequest


def set_briton_request_fields_from_model_input(
    model_input: Dict[str, Any], briton_request: InferenceRequest
):
    for model_input_key, briton_field in MODEL_INPUT_TO_BRITON_FIELD.items():
        if model_input_key in model_input:
            model_input_value = model_input[model_input_key]
            try:
                setattr(briton_request, briton_field, model_input_value)
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
