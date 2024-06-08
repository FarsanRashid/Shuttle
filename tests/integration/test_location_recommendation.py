import logging
from django.test import TestCase
from utils.location_service_provider import LocationServiceProvider
from service_layer import recommend_location


class RecommendLocationTests(TestCase):
    def test_recommended_location_is_returned(self):
        provider = LocationServiceProvider().get_provider()
        response = recommend_location.recommend("buet", provider)
        logging.info(response)
        self.assertIn("places", response)
