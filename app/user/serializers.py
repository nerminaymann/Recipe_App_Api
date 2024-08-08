from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email','password','name']
        extra_kwargs = {
            'password' : {'write_only':True , 'min_length':5}
        }

    def create (self, validated_data):
        #create and return user with encrypted pass
        user = User.objects.create_user(**validated_data)
        return user