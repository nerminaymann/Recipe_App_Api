from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ...core import models
from ..serializers import RecipeSerializer

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
        self.recipes_url = reverse('recipe:recipe-list')

    def test_call_recipe_list_unauthenticated(self):
        #test authentication is required

        res = self.client.get(self.recipes_url)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTest(TestCase):
    #test authenticated user call recipe api request

    def setUp(self):
        self.client = APIClient
        self.recipes_url = reverse('recipe:recipe-list')
        self.user = User.objects.create_user(
            email= 'test@example.com',
            password= '12345'
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_list_recipes_authenticated(self):
        #test retrieve list of recipes

        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(self.recipes_url)

        recipes=models.Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes,many=True)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)


    def test_retrieve_specified_list_recipes_of_authenticated_user(self):
        #test retrieve all the recipes of the authenticated user

        other_user = User.objects.create_user(
            email='test_anotheruser@exampe.com',
            password='12345'
        )

        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(self.recipes_url)

        recipes = models.Recipe.objects.filter(user=self.user).order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)