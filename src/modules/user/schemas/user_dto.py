from fastapi_camelcase import CamelModel


class UserBaseDto(CamelModel):
    first_name: str
    last_name: str
    middle_name: str | None


class UserDto(UserBaseDto):
    id: int

    class Config:
        orm_mode = True
