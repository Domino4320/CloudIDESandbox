from src.cloudidesandbox.core.redis import get_redis_client
from fastapi import Depends
from typing import Annotated
from redis import Redis

RedisDep = Annotated[Redis, Depends(get_redis_client)]
