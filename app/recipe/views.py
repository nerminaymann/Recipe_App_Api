from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import serializers
from ..core import models

# Create your views here.

class RecipeView(viewsets.ModelViewSet):
    #all CRUP operations on Recipe

    serializer_class = serializers.RecipeSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.Recipe.objects.all().order_by('-id')

    def get_queryset(self):
        #to return the recipes of the authenticated user only
        return self.queryset.filter(user=self.request.user).order_by('-id')
