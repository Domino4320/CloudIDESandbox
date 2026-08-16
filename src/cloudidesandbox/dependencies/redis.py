from src.cloudidesandbox.core.redis import get_redis_client
from src.cloudidesandbox.repositories.redis import RedisRepository
from fastapi import Depends
from typing import Annotated
from redis import Redis

RedisDep = Annotated[Redis, Depends(get_redis_client)]


def get_redis_repository(redis: RedisDep) -> RedisRepository:
    redis_repository = RedisRepository(redis=redis)
    return redis_repository


RedisRepositoryDep = Annotated[RedisRepository, Depends(get_redis_repository)]
