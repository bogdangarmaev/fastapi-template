from fastapi import Depends, status
from starlette.responses import Response

from src.modules.user.schemas.user_dto import (
    UserDto,
    UserBaseDto,
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


@user_router.post("/", response_model=UserDto)
async def create_user(
    user: UserBaseDto,
    service: UserService = Depends(UserService),
):
    return await service.create(user)


@user_router.patch("/{id_}", response_model=UserDto)
async def update_user(
    id_: int,
    user: UserBaseDto,
    service: UserService = Depends(UserService),
):
    return await service.update(id_, user)


@user_router.delete("/{id_}", status_code=204)
async def delete_user(
    id_: int,
    service: UserService = Depends(UserService),
):
    await service.delete(id_)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
