from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

User= get_user_model()

def create_user(**params):
    return User.objects.create_user(**params)

class PublicUserApiTests(TestCase):

    def setUp(self):

        self.client = APIClient()
        self.create_user_url = reverse('user:create')

    def test_create_user_successful(self):
        #test user is created successful

        payload = {
            'email':'test@example.com',
            'password':'12345',
            'name':'Test Name'
        }
        res = self.client.post(self.create_user_url,payload)

        self.assertEqual(res.Status_code,status.HTTP_201_CREATED)

        #to validate the user obj is created in the db
        user = User.objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

        #ensure the pass won't return in the response data
        self.assertNotIn('password',res.data)

