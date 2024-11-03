from pydantic import BaseModel

from .base import AppBaseException
from .domain import ValidationException


class UsecaseException(AppBaseException):
    def __init__(self, message: str, error_code: str):
        super().__init__(message, error_code)


class PermissionDeniedException(AppBaseException):
    def __init__(self, message: str, error_code: str):
        super().__init__(message, error_code)


class DtoValidationException(UsecaseException):
    def __init__(
        self,
        e: ValidationException,
        dto_model: BaseModel,
        message: str,
        error_code: str,
    ):
        property_names = set(dto_model.model_fields.keys())
        self.dto_errors = list(
            map(
                lambda err: err.model_dump(),
                filter(
                    lambda err: err.name in property_names,
                    e.multi_validate_errors.readable_errors,
                ),
            )
        )
        super().__init__(message, error_code)
