from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import ProfileUser

User = get_user_model()


class ProfileUserSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя (ProfileUser).

    Назначение:
    - сериализует данные профиля, включая аватарку;
    - предоставляет email пользователя через вложенное поле user_profile;
    - защищает связь профиль → пользователь от изменения со стороны клиента."""

    user_email = serializers.EmailField(source='user_profile.email', read_only=True) #видно email на фронте
    class Meta:
        model = ProfileUser
        fields = ('user_profile', 'user_email', 'image')
        read_only_fields = ('user_profile',)#Пользователь не должен иметь возможность менять, к какому User привязан профиль
