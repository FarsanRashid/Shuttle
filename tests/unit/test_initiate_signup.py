import json
from unittest.mock import MagicMock, patch

from django.test import Client, TestCase
from django.urls import reverse

from adapters.cache import RedisCache
from utils.attributes import (
    CONTACT_NUMBER,
    COUNTRY_DIAL_CODE,
    PASSWORD,
    USERNAME,
    error_invalid_payload,
    error_invalid_request_method,
    error_username_exists,
)


class InitiateSignupTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('initiate_signup')
        self.cache = RedisCache()
        self.data = {
            USERNAME: 'testuser',
            PASSWORD: 'testpassword',
            COUNTRY_DIAL_CODE: 'testcode',
            CONTACT_NUMBER: 'testnumber'
        }

    def tearDown(self) -> None:
        self.cache.delete_all_key()

    def test_initiate_signup_with_missing_fields(self):
        data = self.data.copy()
        data.pop(USERNAME)
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_invalid_payload)

        data = self.data.copy()
        data.pop(PASSWORD)
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_invalid_payload)

        data = self.data.copy()
        data.pop(COUNTRY_DIAL_CODE)
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_invalid_payload)

        data = self.data.copy()
        data.pop(CONTACT_NUMBER)
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_invalid_payload)

    @patch('service_layer.initiate_signup.get_sms_sender', return_value=MagicMock())
    def test_initiate_signup_for_existing_username(self, _):
        _ = self.client.post(self.url, json.dumps(
            self.data), content_type='application/json')
        response = self.client.post(self.url, json.dumps(
            self.data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),  error_username_exists)

    def test_initiate_signup_with_invalid_payload(self):
        data = self.data.copy()
        # contact number is supposed to be a string
        data[CONTACT_NUMBER] = ' '
        response = self.client.post(
            self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),  error_invalid_payload)

        data = self.data.copy()
        # country code is supposed to be a string
        data[COUNTRY_DIAL_CODE] = 880  # type: ignore
        response = self.client.post(
            self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),  error_invalid_payload)

    def test_invalid_request_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(),
                         error_invalid_request_method)
