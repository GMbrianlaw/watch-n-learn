from typing import Generator

from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.session import Session, sessionmaker

DATABASE_ENGINE = create_engine(
    "sqlite:///database.sqlite3", connect_args={"check_same_thread": False}
)

DatabaseSession = sessionmaker(DATABASE_ENGINE, autoflush=False)

def create_session() -> Generator[Session, None, None]:

    session = DatabaseSession()

    try:

        yield session

    finally:
        session.close()
