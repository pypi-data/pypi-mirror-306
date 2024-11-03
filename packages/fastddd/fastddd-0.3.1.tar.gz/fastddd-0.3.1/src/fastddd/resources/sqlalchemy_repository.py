from sqlalchemy import text
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timezone

from .i_base_repository import IBaseRepository


class SessionDeliverer:
    def __init__(self, session: Session) -> None:
        self.__session = session

    def __enter__(self) -> Session:
        return self.__session

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        return


class SessionManager:
    def __init__(self, maker: sessionmaker[Session]) -> None:
        self.__maker = maker

    def __enter__(self) -> Session:
        self.__session = self.__maker()
        return self.__session

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            print(exc_type, exc_val, exc_tb)
            self.__session.rollback()
        self.__session.close()


class SQLAlchemyRepository(IBaseRepository[Session]):
    def __init__(self, sessionmaker: sessionmaker[Session]) -> None:
        self.__sessionmaker = sessionmaker

    def connect(self, session: Session = None) -> SessionManager | SessionDeliverer:
        if session is None:
            return SessionManager(self.__sessionmaker)
        else:
            return SessionDeliverer(session)

    def begin(self) -> Session:
        return self.__sessionmaker()

    def nextval(self, model, session: Session) -> int:
        return session.execute(
            text(f"SELECT nextval('{model.__tablename__}_id_seq')")
        ).scalar()

    def commit(self, session: Session) -> None:
        session.commit()
        session.close()

    def rollback(self, session: Session) -> None:
        session.rollback()
        session.close()

    def close(self, session: Session) -> None:
        session.close()

    def now(self) -> datetime:
        return datetime.now(timezone.utc)
