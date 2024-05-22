import json

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse
import jwt
import redis

from utils.config import REDIS_HOST, REDIS_PORT

from service_layer.services import PendingOtpValidation
from utils.attributes import (
    CONTACT_NUMBER,
    COUNTRY_CODE,
    PASSWORD,
    USERNAME,
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
            USERNAME: 'testuser',
            PASSWORD: 'testpassword',
            COUNTRY_CODE: 'testcode',
            CONTACT_NUMBER: 'testnumber'
        }

    def tearDown(self) -> None:
        self.redis_con.flushdb()

    def test_successful_signup_initiation(self):
        response = self.client.post(self.url, json.dumps(
            self.data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), success_signup_initiate)

        jwt_token = jwt.encode(
            {USERNAME: self.data.get(USERNAME)}, settings.SECRET_KEY)
        self.assertEqual(self.redis_con.exists(jwt_token), 1)

    def test_initiate_signup_with_missing_fields(self):
        data = self.data
        data.pop(USERNAME)
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_field)

        data = self.data
        data.pop(PASSWORD)
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_field)

        data = self.data
        data.pop(COUNTRY_CODE)
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_field)

        data = self.data
        data.pop(CONTACT_NUMBER)
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_field)

    def test_initiate_signup_for_existing_username(self):
        jwt_token = jwt.encode(
            {USERNAME: self.data.get(USERNAME)}, settings.SECRET_KEY)

        pending_otp_validation = PendingOtpValidation(
            self.data.get(USERNAME),
            'testpassword', 1234)
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
