from redis.asyncio import Redis
from src.cloudidesandbox.core.config import redis_config
from src.cloudidesandbox.exceptions.redis import RedisNotInitializedError

redis: Redis | None = None


async def init_redis() -> None:
    global redis
    redis = Redis.from_url(redis_config.REDIS_URL, decode_responses=True)
    await redis.ping()


async def close_redis() -> None:
    global redis
    if redis:
        await redis.aclose()
        redis = None


def get_redis_client() -> Redis:
    if redis:
        return redis
    raise RedisNotInitializedError()
