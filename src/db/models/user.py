from sqlalchemy import Column, String, Integer

from src.db.connection import DeclarativeBase
from src.db.mixins import TimestampMixin


class User(DeclarativeBase, TimestampMixin):
    __tablename__ = "users"
    __table_args__ = {"comment": "Пользователи"}

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Идентификатор пользователя",
    )

    first_name = Column(String, nullable=False, comment="Имя пользователя")
    last_name = Column(String, nullable=False, comment="Фамилия пользователя2")
    middle_name = Column(String, comment="Отчество пользователя")
