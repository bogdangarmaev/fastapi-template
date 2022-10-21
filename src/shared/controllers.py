from typing import Iterable

from fastapi import APIRouter


def api_router_factory(
    postfix: str,
    dependencies: Iterable = None,
    api_prefix: str = "/api/",
) -> APIRouter:
    return APIRouter(
        prefix=f"{api_prefix}{postfix}",
        tags=[postfix],
        dependencies=dependencies if dependencies is not None else [],
    )
