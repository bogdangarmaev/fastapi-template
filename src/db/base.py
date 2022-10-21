import asyncio
from abc import abstractmethod, ABC
from typing import Iterable

from fastapi import Depends
from sqlalchemy import select, insert, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.connection import get_session
from src.shared.db_utils import generate_filters
from src.shared.decorators import check_exist


async def scalar(session, query, is_unique: bool = False):
    result = await session.execute(query)
    if is_unique:
        return result.unique().scalar()
    return result.scalar()


async def scalars(session, query, is_unique: bool = False):
    result = await session.execute(query)
    if is_unique:
        return result.unique().scalars().all()
    return result.scalars().all()


async def scalar_one(session, query, is_unique: bool = False):
    result = await session.execute(query)
    if is_unique:
        return result.unique().scalar_one()
    return result.scalar_one()


class BaseMixin:
    @property
    @abstractmethod
    def model(self):
        raise NotImplementedError

    def __init__(
        self,
        session: AsyncSession = Depends(get_session),
    ):
        self._session_ = session
        self.default_query = select(self.model)
        self.is_unique = False

    async def execute(self, query):
        return await self._session_.execute(query)

    @check_exist
    async def fetch_instance(self, id: int = None, **filters):
        filter_by = generate_filters(id, **filters)
        query = self.default_query.filter_by(**filter_by)

        db_item = await self.execute(query)
        db_item = db_item.scalar()
        return db_item

    async def total(self, query) -> int:
        query = (
            query.select_from(self.model)
            .with_only_columns(func.count(self.model.id).label("total"))
            .group_by(None)
            .order_by(None)
            .limit(None)
            .offset(None)
        )
        result = await self.execute(query)
        total = result.fetchone()
        return total["total"] if total is not None else 0

    async def scalar_(self, query, is_unique: bool = False):
        return await scalar(self._session_, query, is_unique)

    async def scalars_(self, query, is_unique: bool = False):
        return await scalars(self._session_, query, is_unique)

    async def scalar_one_(self, query, is_unique: bool = False):
        return await scalar_one(self._session_, query, is_unique)

    async def fetchone_(self, query):
        cursor = await self.execute(query)
        return cursor.fetchone()

    async def fetchall(self, query):
        cursor = await self.execute(query)
        return cursor.fetchall()


class ReadMixin(BaseMixin, ABC):
    async def all(
        self,
        skip: int | None = 0,
        limit: int | None = 100,
        joins: Iterable = None,
        filters: Iterable = None,
        filter_by: dict = None,
    ):
        query = self.default_query.limit(limit).offset(skip)
        if joins:
            query = query.options(*joins)
        if filters:
            query = query.filter(*filters)
        if filter_by:
            query = query.filter_by(**filter_by)
        return await self.scalars_(query)

    async def get(
        self,
        id: int = None,
        joins: Iterable = None,
        filters: Iterable = None,
        filter_by: dict = None,
    ):
        query = self.default_query
        if id:
            query = query.filter_by(id=id)
        if joins:
            query = query.options(*joins)
        if filters:
            query = query.filter(*filters)
        if filter_by:
            query = query.filter_by(**filter_by)
        return await self.scalar_(query)

    async def all_with_total(
        self,
        skip: int = 0,
        limit: int = 100,
        joins: Iterable = None,
        filters: Iterable = None,
    ):
        query = self.default_query.limit(limit).offset(skip)
        if joins:
            query = query.options(*joins)
        if filters:
            query = query.filter(*filters)
        total, results = await asyncio.gather(
            self.total(self.default_query), self.scalars_(query, True)
        )
        return {
            "total": total,
            "results": results,
        }


class CreateMixin(BaseMixin, ABC):
    async def create(self, item: dict):
        query = insert(self.model).returning(self.model).values(**item)
        return await self.fetchone_(query)

    async def create_many(self, items: list[dict]):
        query = insert(self.model).returning(self.model).values(items)
        return await self.fetchall(query)


class UpdateMixin(BaseMixin, ABC):
    async def update(self, updated_data: dict, id_: int = None, **filters):
        query = (
            update(self.model)
            .returning(self.model)
            .filter_by(**generate_filters(id_, **filters))
            .values(updated_data)
        )

        return await self.fetchone_(query)


class DeleteMixin(BaseMixin, ABC):
    async def delete(self, id_):
        query = delete(self.model).filter_by(id=id_)
        await self.execute(query)
        return None
