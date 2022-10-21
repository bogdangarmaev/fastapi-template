from typing import Generic, Iterable

from pydantic import BaseModel

from src.shared.type_var import TRepository, TModel, TListWithTotal


class CRUDService(Generic[TRepository, TModel]):
    repository: TRepository

    async def get_one(
        self,
        id_: int | None = None,
        filters: Iterable | None = None,
        filter_by: dict | None = None,
    ) -> TModel:
        return await self.repository.get(
            id=id_, filters=filters, filter_by=filter_by
        )

    async def get_many(
        self,
        skip: int | None = None,
        limit: int | None = None,
        filters: Iterable | None = None,
        filter_by: dict | None = None,
    ) -> list[TModel]:
        return await self.repository.all(
            skip, limit, filters=filters, filter_by=filter_by
        )

    async def get_many_with_total(
        self,
        skip: int | None = None,
        limit: int | None = None,
        filters: Iterable | None = None,
    ) -> TListWithTotal:
        return await self.repository.all_with_total(skip, limit, filters)

    async def create(self, item: BaseModel) -> TModel:
        return await self.repository.create(item.dict())

    async def create_many(self, items: list[BaseModel]) -> list[TModel]:
        dicts = [item.dict() for item in items]
        return await self.repository.create_many(dicts)

    async def update(self, id_: int, item: BaseModel) -> TModel:
        return await self.repository.update(item.dict(), id_)

    async def delete(self, id_: int) -> str:
        return await self.repository.delete(id_)
