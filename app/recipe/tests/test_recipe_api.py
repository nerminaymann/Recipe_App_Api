from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ...core import models


User = get_user_model()

def create_recipe(user,**params):
    #Create and Return sample recipe
    default = {
        'title':'sample recipe name',
        'desc':'sample recipe desc',
        'time_minutes':3,
        'price':Decimal('5.50'),
        'link':'exampleRecipe.com'
    }
    default.update(params)
    recipe = models.Recipe.objects.create(user=user,**default)
    return recipe

class PublicRecipeApiTest(TestCase):
    #test when unathenticated user call recipe api request return unathorized error

    def setUp(self):
        self.client = APIClient
        self.recipe_url = reverse('recipe:recipe-list')

    def test_call_recipe_list_unauthenticated(self):
        #test authentication is required

        res = self.client.get(self.recipe_url)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)
