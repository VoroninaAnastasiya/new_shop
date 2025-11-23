from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import ProfileUser

User = get_user_model()
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('name', 'lastname', 'contact_phone', 'email', 'created_at', 'updated_at')


class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = ('user_profile', 'image')
