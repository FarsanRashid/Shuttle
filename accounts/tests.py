import json

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse
import jwt
import redis

from utils.config import REDIS_HOST, REDIS_PORT

from service_layer.services import PendingOtpValidation
from utils.attributes import (
    error_invalid_json,
    error_invalid_request_method,
    error_missing_field,
    error_username_exists,
    success_signup_initiate,
)


class SignupViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('initiate_signup')
        self.redis_con = redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        self.data = {
            'username': 'testuser',
            'password': 'testpassword',
            'country_code': 'testcode',
            'contact_number': 'testnumber'
        }

    def tearDown(self) -> None:
        self.redis_con.flushdb()

    def test_successful_signup_initiation(self):
        response = self.client.post(self.url, json.dumps(
            self.data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), success_signup_initiate)

        jwt_token = jwt.encode(
            {'username': self.data.get('username'), }, settings.SECRET_KEY, algorithm='HS256')
        self.assertEqual(self.redis_con.exists(jwt_token), 1)

    def test_initiate_signup_with_missing_fields(self):
        data = self.data
        data.pop('username')
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_field)

        data = self.data
        data.pop('password')
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_field)

        data = self.data
        data.pop('country_code')
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_field)

        data = self.data
        data.pop('contact_number')
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_field)

    def test_initiate_signup_for_existing_username(self):
        jwt_token = jwt.encode(
            {'username': self.data.get('username')}, settings.SECRET_KEY, algorithm='HS256')

        pending_otp_validation = PendingOtpValidation(
            self.data.get('username'), 'testpassword', otp=1234)
        self.redis_con.set(jwt_token, json.dumps(
            pending_otp_validation._asdict()))

        response = self.client.post(self.url, json.dumps(
            self.data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),  error_username_exists)

    def test_initiate_signup_with_invalid_json(self):
        data = 'invalid json'
        response = self.client.post(
            self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),  error_invalid_json)

    def test_invalid_request_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(),
                         error_invalid_request_method)
