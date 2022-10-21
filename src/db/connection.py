import json
from uuid import UUID

from fastapi import FastAPI
from loguru import logger

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from src.core.config import settings


DeclarativeBase = declarative_base()


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


def generate_session(db_dsn):
    engine = create_async_engine(
        db_dsn,
        echo=settings.db_log_echo,
        json_serializer=lambda obj: json.dumps(
            obj, cls=UUIDEncoder, ensure_ascii=False, default=str
        ),
    )
    return (
        engine,
        sessionmaker(engine, class_=AsyncSession, expire_on_commit=False),
    )


DEFAULT_ENGINE, DEFAULT_SESSION = generate_session(settings.db_dsn)


def setup_db(app: FastAPI) -> None:  # pragma: no cover
    app.state.db_engine = DEFAULT_ENGINE


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with DEFAULT_SESSION() as session:

        try:  # noqa: WPS501
            yield session
            await session.commit()
        except Exception as e:
            logger.error(e)
            await session.rollback()
        finally:
            await session.close()
