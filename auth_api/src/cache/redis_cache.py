from typing import Any, Optional

import redis

from src.cache.base import BaseCache
from src.core.config import redis_settings


redis_db = redis.Redis(host=redis_settings.REDIS_HOST, port=redis_settings.REDIS_PORT, db=0)


class RedisCache(BaseCache):
    def __init__(self, redis: redis.Redis) -> None:
        super().__init__(redis)

    def _get(self, redis_key: str) -> Optional[Any]:
        data = self.redis.get(redis_key)
        if not data:
            return None
        return data.decode()

    def _put_token(self, redis_key: str, identity: str, expire: int) -> None:
        self.redis.set(redis_key, identity, ex=expire)

    def _clear_token(self, redis_key: str) -> None:
        self.redis.delete(redis_key)


redis_cache = RedisCache(redis_db)
