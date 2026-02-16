from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.utils.representation import serializer_repr
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import ProfileUser
from .serializers import ProfileUserSerializer


# Create your views here.
# class UserAPIView(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class ProfileUserListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated] # TODO позже переделать на permission_classes = [IsAdminUser], доступ только у админа
    queryset = ProfileUser.objects.all()
    serializer_class = ProfileUserSerializer


class ProfileUserCreateAPIView(generics.CreateAPIView):
    queryset = ProfileUser.objects.all()
    serializer_class = ProfileUserSerializer


class ProfileUserView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] #позволяет принимать запросы с файлами (multipart/form-data).
    # Без этого картинка просто не попадёт в request.data

    def get(self, request):
        profile, _ = ProfileUser.objects.get_or_create(user_profile=request.user)
        serializer = ProfileUserSerializer(profile)
        return Response(serializer.data)

    def put(self,request): #! TODO доработать метод, чтобы картинка обновлялась
        profile, _ = ProfileUser.objects.get_or_create(user_profile=request.user)
        serializer = ProfileUserSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        profile, _ = ProfileUser.objects.get_or_create(
            user_profile=request.user) #возвращает кортеж из двух значений: (объект, создан_ли_он)
        # _ — это общепринятое обозначение «переменная, которую мы игнорируем»
        # Если аватарки нет — возвращаем сообщение
        if not profile.image:
            return Response({"detail": "Аватарка уже отсутствует."},
                            status=400)

        profile.image.delete(save=False) # Удаляем файл с диска
        profile.image = None # Очищаем поле в базе
        profile.save(update_fields=['image'])

        return Response({"detail": "Аватарка успешно удалена."},
                        status=204)
