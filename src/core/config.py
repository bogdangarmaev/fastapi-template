import enum
from functools import lru_cache

from pydantic import BaseSettings, validator, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    """Конфигурация проекта"""

    app_name: str
    # Debug
    debug: bool
    db_log_echo: bool

    # Конфигурация Postgres
    db_name: str
    db_user: str
    db_host: str
    db_port: str
    db_password: str
    db_dsn: str = None
    sync_db_dsn: str = None

    @validator("db_dsn", pre=True)
    def assemble_db_dsn(cls, v, values):
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=values.get("db_host"),
            port=values.get("db_port"),
            user=values.get("db_user"),
            password=values.get("db_password"),
            path=f"/{values.get('db_name')}",
        )

    @validator("sync_db_dsn", pre=True)
    def assemble_sync_db_dsn(cls, v, values):
        return PostgresDsn.build(
            scheme="postgresql",
            host=values.get("db_host"),
            port=values.get("db_port"),
            user=values.get("db_user"),
            password=values.get("db_password"),
            path=f"/{values.get('db_name')}",
        )

    # Конфигурация Redis
    redis_host: str
    redis_port: str
    redis_username: str = None
    redis_password: str = None

    redis_dsn: str = None

    @validator("redis_dsn", pre=True)
    def assemble_redis_dsn(cls, v, values):
        return RedisDsn.build(
            scheme="redis",
            host=values.get("redis_host"),
            port=values.get("redis_port"),
            user=values.get("redis_username"),
            password=values.get("redis_password"),
        )

    # Конфигурация тестов
    test_db_name: str
    test_db_url: str = None
    test_db_dsn: str = None

    @validator("test_db_url", pre=True)
    def assemble_test_db_url(cls, v, values):
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=values.get("db_host"),
            port=values.get("db_port"),
            user=values.get("db_user"),
            password=values.get("db_password"),
            # path=f"/{values.get('test_db_name')}",
        )

    @validator("test_db_dsn", pre=True)
    def assemble_test_db_dsn(cls, v, values):
        return values.get("test_db_url") + "/" + values.get("test_db_name")

    class Config:
        env_file = ".env"


@lru_cache
def _get_settings(**kwargs) -> Settings:
    return Settings(**kwargs)


settings = _get_settings()
