from django.test import Client, TestCase
from django.urls import reverse

from utils.attributes import (
    error_invalid_request_method
)


class RecommendLocationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('recommend_location')

    def test_invalid_request_method(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(),
                         error_invalid_request_method)
