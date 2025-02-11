from typing import Any, AsyncGenerator

from decouple import config
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base

POSTGRES_DB = config(
    "POSTGRES_DB",
    default="test_merch_db",
    cast=str,
)
POSTGRES_USER = config(
    "POSTGRES_USER",
    default="test_user",
    cast=str,
)
POSTGRES_PASSWORD = config(
    "POSTGRES_PASSWORD",
    default="test_password",
    cast=str,
)
POSTGRES_HOST = config(
    "POSTGRES_HOST",
    default="localhost",
    cast=str,
)
POSTGRES_PORT = config(
    "POSTGRES_PORT",
    default="5432",
    cast=str,
)

SQLALCHEMY_DATABASE_URL: str = (
    f"postgresql+asyncpg://{POSTGRES_USER}"
    f":{POSTGRES_PASSWORD}@{POSTGRES_HOST}"
    f":{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine: AsyncEngine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
)
SessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
Base: Any = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, Any]:
    async with SessionLocal() as db:
        yield db
