from abc import ABC, abstractmethod
import os
import time
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


class FakeCache(AbstractCache):
    def __init__(self):
        self.__store: dict[str, Any] = {}
        self.__ttl_store: dict[str, float] = {}

    def __is_expired(self, key):
        if key in self.__ttl_store:
            if time.time() > self.__ttl_store[key]:
                self.delete(key)
                return True
        return False

    def get(self, key) -> Any:
        if key in self.__store and not self.__is_expired(key):
            return self.__store[key]
        return None

    def set(self, key, value) -> Any:
        self.__store[key] = value
        if key in self.__ttl_store:
            del self.__ttl_store[key]

    def set_if_not_exists(self, key, value) -> Any:
        if key not in self.__store or self.__is_expired(key):
            self.set(key, value)
            return True
        return False

    def set_with_TTL(self, key, value, ttl) -> Any:
        self.set(key, value)
        self.__ttl_store[key] = time.time() + ttl
        return True

    def set_with_TTL_if_not_exists(self, key, value, ttl) -> Any:
        if key not in self.__store or self.__is_expired(key):
            self.set_with_TTL(key, value, ttl)
            return True
        return False

    def delete(self, key) -> Any:
        if key in self.__store:
            del self.__store[key]
        if key in self.__ttl_store:
            del self.__ttl_store[key]

    def delete_all_key(self) -> Any:
        self.__store.clear()
        self.__ttl_store.clear()
