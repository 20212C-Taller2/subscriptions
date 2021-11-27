import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_url():
    if os.environ.get("DATABASE_URL") is not None:
        uri = os.getenv("DATABASE_URL")  # or other relevant config var
        if uri and uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
            return uri
    return os.environ["FASTAPI_POSTGRESQL"]


SQLALCHEMY_DATABASE_URL = get_url()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BaseModelDb = declarative_base()
