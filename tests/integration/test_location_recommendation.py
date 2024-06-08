import logging
from django.test import TestCase
from location.geo_service.geo_service import BariKoi
from service_layer import recommend_location


class RecommendLocationTests(TestCase):
    def test_recommended_location_is_returned(self):
        barikoi = BariKoi()
        response = recommend_location.recommend("buet", barikoi)
        logging.info(response)
        self.assertIn("places", response)
