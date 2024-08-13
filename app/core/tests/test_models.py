"""
test for models
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from ..models import Recipe
from decimal import Decimal


User = get_user_model()

class ModelTests(TestCase):

#-----------------------------------------Test Custom User Model-----------------------------------------------
    def test_create_user_with_email_successful(self):
        email = "test@example.com"
        password = "12345"

        user = User.objects.create_user(email=email,password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_normalized(self):
        sample_emails = [
            ['test1@EXAMPLE.com','test1@example.com'],
            ['test2@example.COM','test2@example.com'],
            ['Test3@Example.com','Test3@example.com'],
            ['TEST4@example.com','TEST4@example.com']
        ]
        password = "12345"

        for email, expected in sample_emails:
            user = User.objects.create_user(email,password)
            self.assertEqual(user.email,expected)


    def test_new_user_without_email_raises_error(self):
        password = '12345'
        with self.assertRaises(ValueError):
            User.objects.create_user('',password)

    def test_create_super_user(self):
        email = 'test@example.com'
        password = '12345'

        user = User.objects.create_superuser(email,password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

#-----------------------------------------Test Recipe Model-----------------------------------------------

    def test_create_recipe_model(self):
        user= User.objects.create_user(
            email='test@example.com',
            name='test user',
            password='12345'
        )

        recipe = Recipe.objects.create(
            user=user,
            title='sample recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            desc='sample recipe description.'
        )

        self.assertEqual(str(recipe),recipe.title)




