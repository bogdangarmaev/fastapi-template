from fastapi import Depends

from src.modules.user.schemas.user_dto import (
    UserDto,
)
from src.modules.user.service import UserService
from src.shared.controllers import api_router_factory
from src.shared.list_queries import ListQueryParams

user_router = api_router_factory("users")


@user_router.get("/", response_model=list[UserDto])
async def get_users(
    query: ListQueryParams = Depends(ListQueryParams),
    service: UserService = Depends(UserService),
):
    return await service.get_many(skip=query.skip, limit=query.limit)


@user_router.get("/{id_}", response_model=UserDto)
async def get_user(
    id_: int,
    service: UserService = Depends(UserService),
):
    return await service.get_one(id_)
