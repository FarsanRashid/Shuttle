import json

from django.test import Client, TestCase
from django.urls import reverse

from utils.attributes import (
    OTP,
    TOKEN,
    error_invalid_request_method,
    error_missing_field,
)


class ValidateSignupTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('validate_signup')
        self.data = {TOKEN: 'testtoken', OTP: 'testotp'}

    def test_invalid_request_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(),
                         error_invalid_request_method)

    def test_valiate_signup_with_missing_fields(self):
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
