import json

from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
import jwt
import redis

from utils.attributes import (
    CONTACT_NUMBER,
    COUNTRY_DIAL_CODE,
    PASSWORD,
    USERNAME,
    success_signup_initiate,
)
from utils.config import REDIS_HOST, REDIS_PORT


class InitiateSignupTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('initiate_signup')
        self.redis_con = redis.Redis(
            host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        self.data = {
            USERNAME: 'farsan',
            PASSWORD: 'testpassword',
            COUNTRY_DIAL_CODE: '880',
            CONTACT_NUMBER: '1674880035'
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