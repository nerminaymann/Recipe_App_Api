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

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

        #to validate the user obj is created in the db
        user = User.objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

        #ensure the pass won't return in the response data
        self.assertNotIn('password',res.data)


    def test_user_with_email_exists_error(self):
        #test error is returned if use email is existed

        payload = {
            'email' : 'test@example.com',
            'password' : '12345',
            'name' : 'User Test'
        }

        create_user(**payload)
        res = self.client.post(self.create_user_url,payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)


    def test_passwrod_too_short_error(self):
        #test error is returned if pass is less than 5 chars

        payload = {
            'email':'test@example.com',
            'password':'123',
            'name':'test user'
        }

        res = self.client.post(self.create_user_url,payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

        user_exists = User.objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)