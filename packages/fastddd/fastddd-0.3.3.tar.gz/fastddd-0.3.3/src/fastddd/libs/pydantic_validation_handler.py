# https://docs.pydantic.dev/latest/errors/errors/
# [
#     {
#         "type": "string_too_short",
#         "loc": ("password",),
#         "msg": "String should have at least 8 characters",
#         "input": "pass",
#         "ctx": {"min_length": 8},
#         "url": "https://errors.pydantic.dev/2.7/v/string_too_short",
#     }
# ]

from typing import List
from enum import Enum
from pydantic import ValidationError, BaseModel


class PydanticErrorType(str, Enum):
    STRING_TOO_SHORT = "string_too_short"
    STRING_TOO_LONG = "string_too_long"
    GREATER_THAN_EQUAL = "greater_than_equal"
    VALUE_ERROR = "value_error"
    MISSING_ERROR = "missing"


class PydanticError(BaseModel):
    type: PydanticErrorType
    loc: tuple
    msg: str
    input: str | int | dict
    ctx: dict | None = None
    url: str | None = None


class PydanticErrors(BaseModel):
    errors: list[PydanticError]


class ReadableError(BaseModel):
    type: PydanticErrorType
    name: str
    msg: str


class MultipleValidateError(BaseModel):
    readable_errors: List[ReadableError]
    pydantic_errors: List[PydanticError]


def convert_pydantic_exception(
    e: ValidationError,
) -> MultipleValidateError:
    print(e.errors())
    errors = PydanticErrors(errors=e.errors())

    readable_errors = []
    pydantic_errors = []

    for error in errors.errors:
        if len(error.loc) == 1:
            if error.type == PydanticErrorType.STRING_TOO_SHORT:
                msg = f"{error.ctx['min_length']}文字以上で入力してください。"
            elif error.type == PydanticErrorType.STRING_TOO_LONG:
                msg = f"{error.ctx['max_length']}文字以内で入力してください。"
            elif error.type == PydanticErrorType.GREATER_THAN_EQUAL:
                msg = f"{error.ctx['ge']}以上で入力してください。"
            elif error.type == PydanticErrorType.VALUE_ERROR:
                if "email address" in error.msg:
                    msg = "正しいメールアドレスを入力してください。"
            elif error.type == PydanticErrorType.MISSING_ERROR:
                msg = "必須項目です。"

            readable_errors.append(
                ReadableError(
                    type=error.type,
                    name=error.loc[0],
                    msg=msg,
                )
            )
        else:
            pydantic_errors.append(error)

    return MultipleValidateError(
        readable_errors=readable_errors, pydantic_errors=pydantic_errors
    )
