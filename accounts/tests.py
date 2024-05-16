import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Passenger


class SignupViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('signup')

    def test_successful_signup(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {
                         'message': 'User created successfully'})
        self.assertTrue(Passenger.objects.filter(username='testuser').exists())

    def test_signup_missing_fields(self):
        data = {
            'username': 'testuser'
            # Missing password
        }
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Missing required fields'})

        data = {
            'password': 'testpassword'
            # Missing username
        }
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Missing required fields'})

    def test_signup_existing_username(self):
        Passenger.objects.create_user(
            username='testuser', password='testpassword')
        data = {
            'username': 'testuser',
            'password': 'newpassword'
        }
        response = self.client.post(self.url, json.dumps(
            data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Username already exists'})

    def test_signup_invalid_json(self):
        data = 'invalid json'
        response = self.client.post(
            self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Invalid JSON'})

    def test_invalid_request_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {'error': 'Invalid request method'})
