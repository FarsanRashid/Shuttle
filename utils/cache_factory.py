import os

from adapters.cache import FakeCache, RedisCache


class CacheFactory:
    _fake_cache = None
    _redis_cache = None
    _is_unit_test_running = os.environ.get("UNIT_TEST_RUNNING", False)

    @classmethod
    def get_cache(cls):
        if cls._is_unit_test_running:
            if cls._fake_cache is None:
                cls._fake_cache = FakeCache()
            return cls._fake_cache
        else:
            if cls._redis_cache is None:
                cls._redis_cache = RedisCache()
            return cls._redis_cache
