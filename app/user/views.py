from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics,authentication,permissions

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import UserSerializer, AuthTokenSerializer


User = get_user_model()

#-----------------------------------REGISTRATION-----------------------------------------
class CreateUserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer


# -----------------------------------UPDATE USER PROFILE-------------------------------------
class UpdateUserView(generics.RetrieveUpdateAPIView):
    #Manage the Authenticated User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_class = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # lookup_field = 'pk'

    def get_object(self):
        return self.request.user



class CreateAuthTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
