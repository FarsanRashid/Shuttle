import json
from typing import Any
from unittest.mock import MagicMock, patch

from django.test import Client, TestCase
from django.urls import reverse

from accounts.models import Passenger
from utils.attributes import (
    CONTACT_NUMBER,
    COUNTRY_DIAL_CODE,
    OTP,
    PASSWORD,
    TOKEN,
    USERNAME,
    error_incorrect_otp,
    error_invalid_payload,
    error_invalid_request_method,
    error_invalid_token,
    success_signup_verification,
)
from utils.cache_factory import CacheFactory


class ValidateSignupTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('validate_signup')
        self.data = {TOKEN: 'testtoken', OTP: 'testotp'}
        cache_factory = CacheFactory()
        self.cache = cache_factory.get_cache()
        self.initiate_signup_payload = {
            USERNAME: 'testuser',
            PASSWORD: 'testpassword',
            COUNTRY_DIAL_CODE: '880',
            CONTACT_NUMBER: '1234567890'
        }

    def tearDown(self) -> None:
        self.cache.delete_all_key()

    def test_validate_signup_with_invalid_request_method(self):
        response: Any = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(),
                         error_invalid_request_method)

    def test_validate_signup_with_missing_payload_fields(self):
        data = self.data.copy()
        data.pop(TOKEN)
        response: Any = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_invalid_payload)

        data = self.data.copy()
        data.pop(OTP)
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_invalid_payload)

    def test_validate_signup_with_incorrect_payload_field_type(self):
        data = self.data.copy()
        # OTP is supposed to be a string
        data[OTP] = 1234  # type: ignore
        response: Any = self.client.post(
            self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),  error_invalid_payload)

        data = self.data.copy()
        # token is supposed to be a string
        data[TOKEN] = 1233  # type: ignore
        response = self.client.post(
            self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),  error_invalid_payload)

    @patch('service_layer.initiate_signup.get_sms_sender', return_value=MagicMock())
    @patch('service_layer.initiate_signup.random.randint')
    def test_validate_signup_token_verification(self, mock_randint, _):
        mock_otp = "1234"
        mock_randint.return_value = mock_otp
        signup_initiate_response: Any = self.client.post(
            reverse('initiate_signup'), self.initiate_signup_payload, content_type='application/json')
        self.assertEqual(signup_initiate_response.status_code, 201)
        # signup initiated successfully

        self.data[OTP] = mock_otp
        self.data[TOKEN] = "invalid.token.value"

        response: Any = self.client.post(self.url,
                                         self.data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),  error_invalid_token)

        self.data[TOKEN] = signup_initiate_response.json()[TOKEN]
        response = self.client.post(self.url,
                                    self.data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),  success_signup_verification)

    @patch('service_layer.initiate_signup.get_sms_sender', return_value=MagicMock())
    @patch('service_layer.initiate_signup.random.randint')
    def test_validate_signup_otp_verification(self, mock_randint, _):
        mock_otp = "1234"
        mock_randint.return_value = mock_otp

        signup_initiate_response: Any = self.client.post(reverse('initiate_signup'), self.initiate_signup_payload,
                                                         content_type='application/json')
        self.assertEqual(signup_initiate_response.status_code, 201)
        # signup initiated successfully

        self.data[TOKEN] = signup_initiate_response.json()[TOKEN]
        self.data[OTP] = "invalid_otp"
        response: Any = self.client.post(self.url,
                                         self.data,
                                         content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_incorrect_otp)

        self.data[OTP] = mock_otp
        response = self.client.post(self.url,
                                    self.data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), success_signup_verification)

    @patch('service_layer.initiate_signup.get_sms_sender', return_value=MagicMock())
    @patch('service_layer.initiate_signup.random.randint')
    def test_signup_validation_creates_new_user(self, mock_randint, _):
        mock_otp = "1234"
        mock_randint.return_value = mock_otp

        signup_initiate_response: Any = self.client.post(reverse(
            'initiate_signup'), self.initiate_signup_payload, content_type='application/json')

        self.data[TOKEN] = signup_initiate_response.json()[TOKEN]
        self.data[OTP] = mock_otp
        _ = self.client.post(self.url,
                             self.data,
                             content_type='application/json')
        username = self.initiate_signup_payload[USERNAME]
        user = Passenger.objects.filter(username=username)
        self.assertEqual(user.count(), 1)
        self.assertEqual(user.first().contact_number,
                         self.initiate_signup_payload[CONTACT_NUMBER])
        self.assertEqual(user.first().country_code,
                         self.initiate_signup_payload[COUNTRY_DIAL_CODE])

    @patch('service_layer.initiate_signup.get_sms_sender', return_value=MagicMock())
    @patch('service_layer.initiate_signup.random.randint')
    def test_signup_validation_success_removes_user_from_pending_list(self, mock_randint, _):
        mock_otp = "1234"
        mock_randint.return_value = mock_otp

        signup_initiate_response: Any = self.client.post(reverse(
            'initiate_signup'), self.initiate_signup_payload, content_type='application/json')

        self.data[TOKEN] = signup_initiate_response.json()[TOKEN]
        self.data[OTP] = mock_otp
        _ = self.client.post(self.url,
                             self.data,
                             content_type='application/json')
        username = self.initiate_signup_payload[USERNAME]
        self.assertEqual(Passenger.objects.filter(
            username=username).count(), 1)
        self.assertIsNone(self.cache.get(self.data[TOKEN]))
