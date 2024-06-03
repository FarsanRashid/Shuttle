import json
from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Passenger
from utils.attributes import (
    error_invalid_request_method,
    error_missing_paramater
)


class RecommendLocationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('recommend_location')
        self.user = Passenger.objects.create_user(
            username='test', password='test')

    def test_invalid_request_method(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(),
                         error_invalid_request_method)

    def test_required_query_parameter_is_provided(self):
        login_response = self.client.post(
            reverse('login'),
            data=json.dumps(
                {'username': 'test', 'password': 'test'}),
            content_type='application/json')

        session_id = login_response.json()['session_id']
        self.client.cookies['sessionid'] = session_id

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_paramater)

        response = self.client.get(self.url, data={'Q': 'test'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_paramater)

        response = self.client.get(self.url, data={'q': 'test'})
        self.assertEqual(response.status_code, 200)

    def test_auth_token_is_provided(self):
        response = self.client.get(self.url, data={'q': 'test'})
        self.assertEqual(response.status_code, 401)

        self.client.cookies['sessionid'] = 'invalid_session_id'
        response = self.client.get(self.url, data={'q': 'test'})
        self.assertEqual(response.status_code, 401)

        response = self.client.post(
            reverse('login'),
            data=json.dumps(
                {'username': 'test', 'password': 'test'}),
            content_type='application/json')

        session_id = response.json()['session_id']
        self.client.cookies['sessionid'] = session_id
        response = self.client.get(self.url, data={'q': 'test'})
        self.assertEqual(response.status_code, 200)
