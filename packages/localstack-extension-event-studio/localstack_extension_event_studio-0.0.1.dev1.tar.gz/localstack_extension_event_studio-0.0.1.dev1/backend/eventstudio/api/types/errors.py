from enum import Enum

from pydantic import BaseModel, ConfigDict


class ErrorType(Enum):
    BOTO_ERROR = "boto_error"
    LOCALSTACK_ERROR = "localstack_error"
    PARAMETER_ERROR = "parameter_error"
    IAM_ERROR = "iam_error"
    LOCALSTACK_WARNING = "localstack_warning"


class InputErrorModel(BaseModel):
    span_id: str
    error_type: ErrorType
    error_message: str


class ErrorModel(InputErrorModel):
    model_config = ConfigDict(from_attributes=True)

    error_id: str
