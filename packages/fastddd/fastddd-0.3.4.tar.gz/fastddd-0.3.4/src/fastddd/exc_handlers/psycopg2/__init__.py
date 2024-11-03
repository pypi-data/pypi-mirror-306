from functools import wraps
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation, ForeignKeyViolation
from typing import Callable, Type

from ...errors.db import DBExceptionTypes

__all__ = ["db_exception_handler"]


def db_exception_handler(
    handler: Callable[[str, str, DBExceptionTypes], Type[BaseException]],
):
    """
    デコレータ: PostgreSQLのIntegrityErrorをハンドリングし、指定された例外をraiseする

    Args:
        handler (Callable[[str, str, DBExceptionType], Type[BaseException]])
            例外をハンドリングする関数

            handlerの引数:
            - 第一引数: テーブル名
            - 第二引数: カラム名
            - 第三引数: 例外のタイプ (DBExceptionType)

            handerの返り値:
            - 例外のクラス
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except IntegrityError as e:
                if isinstance(e.orig, UniqueViolation):
                    msg = e.orig.diag.message_detail
                    table_name = e.orig.diag.table_name
                    column_name = msg.split("(")[1].split(")")[0]
                    raise handler(
                        table_name, column_name, DBExceptionTypes.UNIQUE_VIOLATION
                    )
                if isinstance(e.orig, ForeignKeyViolation):
                    msg = e.orig.diag.message_detail
                    table_name = e.orig.diag.table_name
                    column_name = msg.split("(")[1].split(")")[0]
                    raise handler(
                        table_name, column_name, DBExceptionTypes.FOREIGN_KEY_VIOLATION
                    )
                raise

        return wrapper

    return decorator
