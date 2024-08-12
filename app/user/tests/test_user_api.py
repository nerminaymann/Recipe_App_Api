from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


def create_user(**params):
    return User.objects.create_user(**params)


#---------------------------for unauthenticated tests to the endpoints----------------------------
class PublicUserApiTests(TestCase):
    #to make unauthenticated requests which don't need authentication
    def setUp(self):
        self.client = APIClient()
        self.create_user_url = reverse('user:create')
        self.token_url = reverse('user:token')
        self.me_url = reverse('user:me')

    def test_create_user_successful(self):
        #test user is created successful

        payload = {
            'email': 'test@example.com',
            'password': '12345',
            'name': 'Test Name'
        }
        res = self.client.post(self.create_user_url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        #to validate the user obj is created in the db
        user = User.objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

        #ensure the pass won't return in the response data
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        #test error is returned if email is existed

        payload = {
            'email': 'test@example.com',
            'password': '12345',
            'name': 'User Test'
        }

        create_user(**payload)
        res = self.client.post(self.create_user_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        #test error is returned if pass is less than 5 chars

        payload = {
            'email': 'test@example.com',
            'password': '123',
            'name': 'test user'
        }

        res = self.client.post(self.create_user_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = User.objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_generate_token_for_user_success(self):
        #test generates valid token for valid credentials
        user_details = {
            'name': 'test user',
            'email': 'test@example.com',
            'password': '12345'
        }
        create_user(**user_details)

        payload = {
            'email': 'test@example.com',
            'password': '12345'
        }
        res = self.client.post(self.token_url, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_generate_token_bad_credentials(self):
        #test return error if credentials invalid

        create_user(email='test@example.com', password='12345')

        payload = {
            'email': 'test@example.com',
            'password': 'badpass'
        }
        res = self.client.post(self.token_url, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_token_blank_password(self):
        #test return error when password field is empty

        create_user(email='test@example.com', password='12345')
        payload = {
            'email': 'test@example.com',
            'password': '',
        }
        res = self.client.post(self.token_url, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        #test return error when the user is unauthenticated
        res = self.client.get(self.me_url)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


#---------------------------for authenticated tests to the endpoints----------------------------
class PrivateUserApiTests(TestCase):
    #test API requests that require authentication
    def setUp(self):
        self.me_url = reverse('user:me')
        self.client = APIClient()

        self.user = create_user(
            email = 'test@example.com',
            name = 'test user',
            password = '12345'
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_authenticated_user(self):
        #retrieve the profile of logged-in user

        res = self.client.get(self.me_url)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,{
            'email':self.user.email,
            'name':self.user.name
        })

    def test_post_me_not_allowed(self):
        #test POST METHOD is not allowed the the endpoint me_url
        res = self.client.post(self.me_url,{})

        self.assertEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_authenticated_user_success(self):
        #test update user profile for authenticated user

        payload = {
            'name': 'updated test user',
            'password': 'updatedpass'
        }

        updated_user_res = self.client.patch(self.me_url,payload)

        #refresh to get the updated data from db
        self.user.refresh_from_db()

        self.assertEqual(self.user.name,payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(updated_user_res.status_code,status.HTTP_200_OK)



