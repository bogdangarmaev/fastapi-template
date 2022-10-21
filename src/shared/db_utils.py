from typing import Iterable

from sqlalchemy import inspect
from sqlalchemy_utils import create_database, database_exists

from src.core.config import settings


def generate_filters(id: int = None, filters: Iterable = None) -> dict:
    filter_by = dict(id=id)
    if id is None:
        filter_by = {*filters}
    return filter_by


def sqlalchemy_model_to_dict(model) -> dict:
    return {
        c.key: getattr(model, c.key)
        for c in inspect(model).mapper.column_attrs
    }


def create_db_if_not_exists():
    db_url = settings.sync_db_dsn
    if not database_exists(db_url):
        create_database(db_url)
