from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import config
from app.utils.json import dumps

engine = create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    json_serializer=dumps,
    pool_size=config.SQLALCHEMY_POOL_SIZE,
)

DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class ManagedSession:
    def __init__(self):
        self.db = DBSession()

    def __enter__(self) -> Session:
        return self.db

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        self.db.close()


def get_db() -> Generator[Session, None, None]:
    try:
        db = DBSession()
        yield db
    finally:
        db.close()
