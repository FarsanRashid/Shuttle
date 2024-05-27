import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from utils.attributes import (
    PASSWORD,
    USERNAME,
    error_invalid_credentials,
    error_invalid_request_method,
    error_missing_field,
    success_login,
)


class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.username = 'testuser'
        self.password = 'testpassword'
        self.login_data = {
            USERNAME: self.username,
            PASSWORD: self.password
        }
        self.user = self.user_model.objects.create_user(
            username=self.username,
            password=self.password,
            country_code='+1',
            contact_number='1234567890'
        )
        self.login_url = reverse('login')

    def test_login_invalid_request_method(self):
        response = self.client.get(
            self.login_url,
            data=self.login_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(),
                         error_invalid_request_method)

    def test_login_missing_fields(self):
        data = self.login_data
        data.pop(USERNAME)
        response = self.client.post(
            self.login_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_field)

        data = self.login_data
        data.pop(PASSWORD)
        response = self.client.post(
            self.login_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), error_missing_field)

    def test_login_success(self):
        response = self.client.post(self.login_url,
                                    data=json.dumps(self.login_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), success_login)

    def test_login_with_invalid_credentials(self):

        self.login_data[PASSWORD] = 'wrongpassword'

        response = self.client.post(
            self.login_url,
            data=json.dumps(self.login_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(error_invalid_credentials, response.json())
