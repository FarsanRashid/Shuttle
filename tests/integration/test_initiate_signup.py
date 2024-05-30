import json

from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
import jwt

from adapters.cache import RedisCache
from utils.attributes import (
    CONTACT_NUMBER,
    COUNTRY_DIAL_CODE,
    PASSWORD,
    USERNAME,
    success_signup_initiate,
)


class InitiateSignupTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('initiate_signup')
        self.cache = RedisCache()
        self.data = {
            USERNAME: 'farsan',
            PASSWORD: 'testpassword',
            COUNTRY_DIAL_CODE: '880',
            CONTACT_NUMBER: '1674880035'
        }

    def tearDown(self) -> None:
        self.cache.delete_all_key()

    def test_successful_signup_initiation(self):
        response = self.client.post(self.url, json.dumps(
            self.data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), success_signup_initiate)

        jwt_token = jwt.encode(
            {USERNAME: self.data.get(USERNAME)}, settings.SECRET_KEY)
        self.assertEqual(self.cache.exists(jwt_token), 1)
