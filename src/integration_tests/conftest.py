import asyncio
from contextlib import suppress
import sys

# https://stackoverflow.com/questions/54895002/modulenotfounderror-with-pytest
from loguru import logger

sys.path.append(".")

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import _get_settings
from src.core.main import app
from src.db.connection import DeclarativeBase, get_session

# чтобы миграции увидели все модели
from src.db.models import *

settings = _get_settings(debug=True)


engine = create_async_engine(settings.test_db_url)
SessionTesting = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


# https://github.com/pytest-dev/pytest-asyncio/issues/68
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def create_test_db() -> None:
    root_engine = create_async_engine(settings.test_db_url)
    async with root_engine.begin() as conn:
        await conn.execute(text("commit;"))
        with suppress(ProgrammingError):
            await conn.execute(
                text(f"create database {settings.test_db_name};")
            )


@pytest.fixture(scope="session", autouse=True)
async def migrations(create_test_db) -> None:
    """
    Create a fresh database on each test case.
    """
    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.drop_all)


@pytest.fixture()
async def session() -> SessionTesting:
    connection = await engine.connect()
    transaction = await connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest.fixture()
async def client(session: SessionTesting) -> AsyncClient:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    async def _get_session() -> AsyncSession:
        yield session

    app.dependency_overrides[get_session] = _get_session
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
