import json
from typing import Any

from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Passenger
from location.geo_service import geo_service
from service_layer import recommend_location
from service_layer.exceptions import SearchQueryTooShortError
from utils.attributes import (
    TOKEN,
    error_invalid_request_method,
    error_invalid_token,
    error_missing_paramater,
)


class RecommendLocationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('recommend_location')
        self.user = Passenger.objects.create_user(  # type:ignore
            username='test', password='test')

    def test_invalid_request_method(self):
        response: Any = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(),
                         error_invalid_request_method)

    def test_required_query_parameter_is_provided(self):
        login_response: Any = self.client.post(
            reverse('login'),
            data=json.dumps(
                {'username': 'test', 'password': 'test'}),
            content_type='application/json')

        token = login_response.json()[TOKEN]

        response: Any = self.client.get(self.url, HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_paramater)

        response = self.client.get(
            self.url, data={'Q': 'test'}, HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_paramater)

        response = self.client.get(
            self.url, data={'q': 'test'},  HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)

    def test_token_authentication(self):
        response: Any = self.client.get(self.url, data={'q': 'test'})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), error_invalid_token)

        response = self.client.get(self.url, data={'q': 'test'},
                                   HTTP_AUTHORIZATION='invalid_token')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), error_invalid_token)

        login_response: Any = self.client.post(
            reverse('login'),
            data=json.dumps(
                {'username': 'test', 'password': 'test'}),
            content_type='application/json')

        token = login_response.json()[TOKEN]
        response = self.client.get(
            self.url, data={'q': 'test'}, HTTP_AUTHORIZATION=token)
        self.assertEqual(response.status_code, 200)

    def test_query_parameter_is_sanitized(self):
        input = 'Test'
        response = recommend_location.sanitize(input)
        self.assertEqual(response, 'test')

        input = ' test_with_space '
        response = recommend_location.sanitize(input)
        self.assertEqual(response, 'test_with_space')

    def test_query_parameter_lenght_is_above_threshold(self):
        input = 'te'
        with self.assertRaises(SearchQueryTooShortError):
            recommend_location.sanitize(input)

    def test_recommended_places_returned(self):
        location_service = geo_service.FakeGeoService()
        response = recommend_location.recommend("buet", location_service)
        self.assertIn("places", response)
