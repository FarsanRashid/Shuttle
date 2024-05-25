import json
import redis
from unittest.mock import MagicMock, patch

from django.test import Client, TestCase
from django.urls import reverse

from service_layer.initiate_signup import error_invalid_json
from utils.attributes import CONTACT_NUMBER, COUNTRY_DIAL_CODE, PASSWORD, USERNAME, error_invalid_json, error_invalid_token
from utils.attributes import (
    OTP,
    TOKEN,
    error_invalid_request_method,
    error_missing_field,
)
from utils.config import REDIS_HOST, REDIS_PORT


class ValidateSignupTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('validate_signup')
        self.data = {TOKEN: 'testtoken', OTP: 'testotp'}
        self.redis_con = redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    def tearDown(self) -> None:
        self.redis_con.flushdb()

    def test_invalid_request_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(),
                         error_invalid_request_method)

    def test_validate_signup_with_missing_fields(self):
        data = self.data
        data.pop(TOKEN)
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_field)

        data = self.data
        data.pop(OTP)
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_field)

    def test_validate_signup_with_invalid_json(self):
        data = self.data
        # OTP is supposed to be a string
        data[OTP] = 1234  # type: ignore
        response = self.client.post(
            self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),  error_invalid_json)

        data = self.data
        # token is supposed to be a string
        self.data[TOKEN] = 1233  # type: ignore
        response = self.client.post(
            self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),  error_invalid_json)

    @patch('service_layer.initiate_signup.get_sms_sender', return_value=MagicMock())
    def test_validate_signup_with_invalid_token(self, _):
        initiate_signup_payload = {
            USERNAME: 'testuser',
            PASSWORD: 'testpassword',
            COUNTRY_DIAL_CODE: '880',
            CONTACT_NUMBER: '1234567890'
        }
        signup_initiate_response = self.client.post(
            reverse('initiate_signup'), initiate_signup_payload, content_type='application/json')
        self.assertEqual(signup_initiate_response.status_code, 201)
        # signup initiated successfully

        self.data[TOKEN] = "invalid.token.value"

        response = self.client.post(self.url,
                                    self.data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),  error_invalid_token)

    @patch('service_layer.initiate_signup.get_sms_sender', return_value=MagicMock())
    def test_validate_signup_with_valid_token(self, _):
        initiate_signup_payload = {
            USERNAME: 'testuser',
            PASSWORD: 'testpassword',
            COUNTRY_DIAL_CODE: "880",
            CONTACT_NUMBER: '1234567890'
        }
        signup_initiate_response = self.client.post(reverse('initiate_signup'), initiate_signup_payload,
                                                    content_type='application/json')
        self.assertEqual(signup_initiate_response.status_code, 201)
        # signup initiated successfully

        self.data[TOKEN] = signup_initiate_response.json()[TOKEN]
        response = self.client.post(self.url,
                                    self.data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
