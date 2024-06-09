import os

from adapters.geo_services import BariKoi, FakeGeoService, GeoService


class LocationServiceFactory:
    _fake_service = None
    _bari_koi = None
    _is_unit_test_running = os.environ.get("UNIT_TEST_RUNNING", False)

    @classmethod
    def get_service(cls) -> GeoService:
        if cls._is_unit_test_running:
            if cls._fake_service is None:
                cls._fake_service = FakeGeoService()
            return cls._fake_service
        else:
            if cls._bari_koi is None:
                cls._bari_koi = BariKoi()
            return cls._bari_koi
