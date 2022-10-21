from abc import ABCMeta
from typing import Type

from factory import Factory
from httpx import AsyncClient

from src.db.connection import DeclarativeBase
from src.integration_tests.conftest import SessionTesting
from src.integration_tests.shared import generate_dict_factory


class BaseTest:
    @property
    def factory(self) -> Type[Factory]:
        raise NotImplementedError

    @property
    def url(self) -> str:
        raise NotImplementedError

    async def _insert_test_item(
        self, session: SessionTesting, factory: Type[Factory] | None = None
    ) -> DeclarativeBase:
        """Создание в БД тестовых данных"""
        if factory is None:
            factory = self.factory
        db_item = factory()
        session.add(db_item)
        await session.flush()
        await session.refresh(db_item)
        return db_item

    async def _generate_post_data(self, session, **kwargs) -> dict:
        """Генерация данных для POST запросов

        Args:
            **kwargs: Поля для переопределения, которые принимает factory.Factory
        """
        return self._generate_data(**kwargs)

    async def _generate_put_data(self, session, **kwargs) -> dict:
        """Генерация данных для PUT запросов

        Args:
            **kwargs: Поля для переопределения, которые принимает factory.Factory
        """
        return self._generate_data(**kwargs)

    def _generate_data(self, **kwargs) -> dict:
        ItemDictFactory = generate_dict_factory(self.factory)
        return ItemDictFactory(**kwargs)


class RetrieveListTest(BaseTest, metaclass=ABCMeta):
    async def test_list(self, client: AsyncClient, session: SessionTesting):
        await self._insert_test_item(session)
        response = await client.get(self.url)
        assert response.status_code == 200, response.status_code


class RetrieveTest(BaseTest, metaclass=ABCMeta):
    async def test_get(self, client: AsyncClient, session: SessionTesting):
        db_item = await self._insert_test_item(session)
        response = await client.get(self.url + str(db_item.id))
        assert response.status_code == 200, response.status_code


class CreateTest(BaseTest, metaclass=ABCMeta):
    async def test_post(self, client: AsyncClient, session: SessionTesting):
        response = await client.post(
            self.url, json=await self._generate_post_data(session)
        )
        assert response.status_code == 200, response.status_code


class UpdateTest(BaseTest, metaclass=ABCMeta):
    async def test_put(self, client: AsyncClient, session: SessionTesting):
        db_item = await self._insert_test_item(session)
        response = await client.put(
            self.url + str(db_item.id),
            json=await self._generate_put_data(session),
        )
        assert response.status_code == 200, response.status_code


class DestroyTest(BaseTest, metaclass=ABCMeta):
    async def test_delete(self, client: AsyncClient, session: SessionTesting):
        db_item = await self._insert_test_item(session)
        response = await client.delete(
            self.url + str(db_item.id),
        )
        assert response.status_code == 204, response.status_code


class CRUDTest(
    CreateTest,
    RetrieveListTest,
    RetrieveTest,
    UpdateTest,
    DestroyTest,
    metaclass=ABCMeta,
):
    pass
