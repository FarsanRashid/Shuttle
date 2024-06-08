import os

from location.geo_service.geo_service import BariKoi, FakeGeoService


class LocationServiceProvider:
    _fake_service = None
    _bari_koi = None
    _is_unit_test_running = os.environ.get("UNIT_TEST_RUNNING", False)

    @classmethod
    def get_provider(cls):
        if cls._is_unit_test_running:
            if cls._fake_service is None:
                cls._fake_service = FakeGeoService()
            return cls._fake_service
        else:
            if cls._bari_koi is None:
                cls._bari_koi = BariKoi()
            return cls._bari_koi
