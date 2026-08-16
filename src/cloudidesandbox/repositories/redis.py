from redis.asyncio import Redis
from datetime import timedelta


class RedisRepository:

    def __init__(self, redis: Redis):
        self.redis = redis

    async def set_pair(self, key: str, value: str) -> None:
        await self.redis.set(key, value)

    async def get_value(self, key: str) -> str | None:
        return await self.redis.get(key)

    async def set_with_expiration(self, key: str, value: str, expiration: timedelta):
        await self.redis.set(key, value, ex=expiration)
