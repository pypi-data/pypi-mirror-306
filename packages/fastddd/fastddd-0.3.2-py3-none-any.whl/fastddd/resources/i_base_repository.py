from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from datetime import datetime

# Sessionはジェネリクスで型を指定する
Session = TypeVar("Session")


class IBaseRepository(Generic[Session], ABC):
    @abstractmethod
    def begin(self) -> Session:
        pass

    @abstractmethod
    def nextval(self, model, session: Session) -> int:
        pass

    @abstractmethod
    def commit(self, session: Session) -> None:
        pass

    @abstractmethod
    def rollback(self, session: Session) -> None:
        pass

    @abstractmethod
    def close(self, session: Session) -> None:
        pass

    @abstractmethod
    def now(self) -> datetime:
        pass
