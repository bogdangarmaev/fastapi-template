import asyncio
import functools
import traceback

from fastapi import HTTPException, status
from loguru import logger
from pydantic import ValidationError
from sqlalchemy import exc

from src.shared.exceptions import NotFoundException


def _check_exist():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            result = await func(*args, **kwargs)
            if result is None:
                raise NotFoundException
            return result

        return wrapped

    return wrapper


check_exist = _check_exist()


def _check_enum_exist():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
            except exc.DBAPIError:
                raise NotFoundException
            else:
                return result

        return wrapped

    return wrapper


check_enum_exist = _check_enum_exist()


def exception_logger(exception_text: str):
    def decorate(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception:
                tb = traceback.format_exc()
                logger.error(f"Exception: {exception_text}\nTraceback:\n{tb}")

        return wrapped

    return decorate


def validation_error_to_client(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exception),
            )

    return wrapper


def retry(retries=5, timeout=10):
    """
    Декоратор для повторной попытки вызовы функции с таймаутом.
    """

    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            for attempt in range(retries - 1):
                try:
                    return await func(*args, **kwargs)
                except Exception:
                    await asyncio.sleep(timeout)
                return await func(*args, **kwargs)

        return wrapped

    return wrapper
