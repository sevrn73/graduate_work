import abc

import redis


class BaseCache:
    def __init__(self, redis: redis.Redis) -> None:
        self.redis = redis

    @abc.abstractmethod
    def _get(self, redis_key: str):
        pass

    @abc.abstractmethod
    def _put_token(self, redis_key: str, identity: str, expire: int) -> None:
        pass

    @abc.abstractmethod
    def _clear_token(self, redis_key: str) -> None:
        pass
