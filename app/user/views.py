from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import UserSerializer


class CreateUserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer