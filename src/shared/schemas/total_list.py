from typing import Generic, TypeVar
from pydantic.generics import GenericModel
from fastapi_camelcase import CamelModel

TDto = TypeVar("TDto", bound=CamelModel)


class ListTotalDto(GenericModel, Generic[TDto]):
    total: int
    results: list[TDto]
