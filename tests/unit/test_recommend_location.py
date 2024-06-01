from django.test import Client, TestCase
from django.urls import reverse

from utils.attributes import (
    error_invalid_request_method,
    error_missing_paramater
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

    def test_required_query_parameter_is_provided(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_paramater)

        response = self.client.get(self.url, data={'Q': 'test'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_paramater)

        response = self.client.get(self.url, data={'q': 'test'})
        self.assertEqual(response.status_code, 200)
