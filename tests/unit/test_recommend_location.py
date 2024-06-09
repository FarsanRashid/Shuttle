import json
from typing import Any

from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Passenger
from service_layer import recommend_location
from utils.attributes import (
    TOKEN,
    error_invalid_request_method,
    error_invalid_token,
    error_missing_paramater,
    error_query_string_too_short,
    success_location_recommended,
)
from utils.cache_factory import CacheFactory
from utils.geo_service_factory import GeoServiceFactory


class RecommendLocationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('recommend_location')
        self.user = Passenger.objects.create_user(  # type:ignore
            username='test', password='test')

        login_response: Any = self.client.post(
            reverse('login'),
            data=json.dumps(
                {'username': 'test', 'password': 'test'}),
            content_type='application/json')

        self.token = login_response.json()[TOKEN]

    def test_invalid_request_method(self):
        response: Any = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(),
                         error_invalid_request_method)

    def test_required_query_parameter_is_provided(self):
        response: Any = self.client.get(
            self.url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_paramater)

        response = self.client.get(
            self.url, data={'Q': 'test'}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_paramater)

        response = self.client.get(
            self.url, data={'q': 'test'},  HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)

    def test_token_authentication(self):
        response: Any = self.client.get(self.url, data={'q': 'test'})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), error_invalid_token)

        response = self.client.get(self.url, data={'q': 'test'},
                                   HTTP_AUTHORIZATION='invalid_token')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), error_invalid_token)

        response = self.client.get(
            self.url, data={'q': 'test'}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 200)

    def test_query_parameter_is_sanitized(self):
        input = 'Test'
        response = recommend_location.sanitize(input)
        self.assertEqual(response, 'test')

        input = ' test_with_space '
        response = recommend_location.sanitize(input)
        self.assertEqual(response, 'test_with_space')

    def test_query_parameter_lenght_is_above_threshold(self):
        seed_location = 'te'
        response = self.client.get(
            self.url, data={'q': seed_location}, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_query_string_too_short)

    def test_recommended_places_returned(self):
        response = self.client.get(
            self.url, data={'q': 'test'}, HTTP_AUTHORIZATION=self.token)

        self.assertEqual(response.status_code, 200)

        self.assertIn("places", response.json())

        self.assertIn(response.json()["code"],
                      success_location_recommended["code"])
        self.assertIn(response.json()["message"],
                      success_location_recommended["message"])
        self.assertIn(response.json()["status"],
                      success_location_recommended["status"])

    def test_recommendations_are_cached(self):
        cache = CacheFactory.get_cache()
        _ = self.client.get(
            self.url, data={'q': 'polasi'}, HTTP_AUTHORIZATION=self.token)
        self.assertIsNotNone(cache.get('polasi'))

    def test_cached_recommendations_returned(self):
        cache = CacheFactory.get_cache()
        cache.set('polasi', 'cached_value')
        geo_service = GeoServiceFactory().get_service()
        response = recommend_location.recommend(
            'polasi', geo_service, cache)
        self.assertEqual(response, 'cached_value')
