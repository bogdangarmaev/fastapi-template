from typing import TypeVar, TypedDict

from src.db.connection import DeclarativeBase
from src.db.repositories import CRUDRepository

TRepository = TypeVar("TRepository", bound=CRUDRepository)

TModel = TypeVar("TModel", bound=DeclarativeBase)


class TListWithTotal(TypedDict):
    list: TModel
    total: int
