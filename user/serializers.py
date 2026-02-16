from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import ProfileUser

User = get_user_model()
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('name', 'lastname', 'contact_phone', 'email', 'created_at', 'updated_at')


class ProfileUserSerializer(serializers.ModelSerializer):
    # email видно на фронте
    user_email = serializers.EmailField(source='user_profile.email', read_only=True)
    class Meta:
        model = ProfileUser
        fields = ('user_profile', 'user_email', 'image')
        read_only_fields = ('user_profile',)#Пользователь не должен иметь возможность менять, к какому User привязан профиль
