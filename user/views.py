from django.shortcuts import render
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
    queryset = ProfileUser.objects.all()
    serializer_class = ProfileUserSerializer


class ProfileUserCreateAPIView(generics.CreateAPIView):
    queryset = ProfileUser.objects.all()
    serializer_class = ProfileUserSerializer


class ProfileUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, _ = ProfileUser.objects.get_or_create(user_profile=request.user)
        serializer = ProfileUserSerializer(profile)
        return Response(serializer.data)

    def put(self,request):
        profile, _ = ProfileUser.objects.get_or_create(user_profile=request.user)
        serializer = ProfileUserSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)