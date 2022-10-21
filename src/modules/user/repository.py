from src.db.models import User
from src.db.repositories import CRUDRepository


class UserRepository(CRUDRepository):
    model = User
