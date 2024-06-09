import logging
from django.test import TestCase
from service_layer import recommend_location
from utils.cache_factory import CacheFactory
from utils.geo_service_factory import GeoServiceFactory


class RecommendLocationTests(TestCase):
    def setUp(self):
        self.cache = CacheFactory().get_cache()

    def tearDown(self) -> None:
        self.cache.delete_all_key()

    def test_recommended_location_is_returned(self):
        geo_service = GeoServiceFactory().get_service()
        response = recommend_location.recommend(
            "buet", geo_service, self.cache)
        logging.info(response)
        self.assertIsInstance(response, list)
