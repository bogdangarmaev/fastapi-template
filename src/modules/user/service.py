from fastapi import Depends

from src.core.service import CRUDService
from src.db.models.user import User
from src.modules.user.repository import UserRepository


class UserService(CRUDService[UserRepository, User]):
    def __init__(
        self, user_repository: UserRepository = Depends(UserRepository)
    ):
        self.repository = user_repository
