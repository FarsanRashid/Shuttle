from abc import ABC, abstractmethod
import os
from typing import Any

import redis


class AbstractCache(ABC):
    @abstractmethod
    def get(self, key) -> Any:
        pass

    @abstractmethod
    def set(self, key, value) -> Any:
        pass

    @abstractmethod
    def set_if_not_exists(self, key, value) -> Any:
        pass

    @abstractmethod
    def set_with_TTL(self, key, value, ttl) -> Any:
        pass

    @abstractmethod
    def set_with_TTL_if_not_exists(self, key, value, ttl) -> Any:
        pass

    @abstractmethod
    def delete(self, key) -> Any:
        pass

    @abstractmethod
    def delete_all_key(self) -> Any:
        pass


class RedisCache(AbstractCache):
    def __init__(self):
        host = os.getenv("REDIS_HOST", "localhost")
        port = int(os.getenv("REDIS_PORT", 6379))
        self.__con = redis.Redis(
            host=host, port=port, decode_responses=True)

    def get(self, key):
        return self.__con.get(key)

    def set(self, key, value):
        return self.__con.set(key, value)

    def set_if_not_exists(self, key, value):
        return self.__con.set(key, value, nx=True)

    def set_with_TTL(self, key, value, ttl):
        return self.__con.set(key,  value, ex=ttl)

    def set_with_TTL_if_not_exists(self, key, value, ttl):
        return self.__con.set(key, value,  nx=True, ex=ttl)

    def delete(self, key):
        return self.__con.delete(key)

    def delete_all_key(self):
        return self.__con.flushdb()
