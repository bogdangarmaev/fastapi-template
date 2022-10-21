from abc import ABC

from src.db.base import ReadMixin, CreateMixin, UpdateMixin, DeleteMixin


class CRUDRepository(ReadMixin, CreateMixin, UpdateMixin, DeleteMixin, ABC):
    ...
