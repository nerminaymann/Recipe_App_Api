"""
test for models
"""
from django.contrib.auth import get_user_model
from django.test import TestCase


User = get_user_model()

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = "test@example.com"
        password = "12345"

        user = User.objects.create_user(email=email,password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


