import redis as _redis
import redis.asyncio as aioredis
from loguru import logger
from src.core.config import settings


redis = aioredis.from_url(settings.redis_dsn)


sync_redis = _redis.Redis(
    host=settings.redis_host,
    username=settings.redis_username,
    password=settings.redis_password,
)


async def check_redis() -> bool:
    status = await redis.ping()
    logger.debug(f"Redis connection status: {status}")
    return status
