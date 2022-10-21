from fastapi import Query
from pydantic import NonNegativeInt, PositiveInt


class ListQueryParams:
    def __init__(
        self,
        skip: NonNegativeInt = Query(default=0),
        limit: PositiveInt = Query(default=100),
    ):
        self.skip = skip
        self.limit = limit
