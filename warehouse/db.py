from pydantic import BaseSettings, Field, PostgresDsn
from sqlalchemy import create_engine
from sqlalchemy.orm import as_declarative, sessionmaker


class DbSettings(BaseSettings):
    DB_URL: PostgresDsn = Field(default="postgresql://guest:guest@db:5432/guest")


engine = create_engine(DbSettings().DB_URL, future=True)

Session = sessionmaker(bind=engine)


def setup_database() -> None:
    Base.metadata.create_all(engine)  # type: ignore


@as_declarative()
class Base:
    def __init__(self, *args, **kwargs) -> None:
        pass
