from enum import Enum, auto

__all__ = ['DBExceptionTypes']


class DBExceptionTypes(Enum):
    UNIQUE_VIOLATION = auto()
    FOREIGN_KEY_VIOLATION = auto()
