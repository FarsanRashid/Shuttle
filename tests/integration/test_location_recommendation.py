import logging
from django.test import TestCase
from utils.location_service_provider import LocationServiceFactory
from service_layer import recommend_location


class RecommendLocationTests(TestCase):
    def test_recommended_location_is_returned(self):
        provider = LocationServiceFactory().get_service()
        response = recommend_location.recommend("buet", provider)
        logging.info(response)
        self.assertIn("places", response)
