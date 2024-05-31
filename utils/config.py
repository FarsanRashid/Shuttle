import os
from adapters.cache import RedisCache, FakeCache
SIGNUP_OTP_TTL = 300

fake_cache = FakeCache()


def get_cache():
    if os.environ.get("UNIT_TEST_RUNNING", False):
        return fake_cache
    return RedisCache()
