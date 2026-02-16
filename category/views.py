from django.shortcuts import render
from rest_framework import generics

from category.models import Category
from category.serializers import CategorySerializer


class CategoryAPIView(generics.ListCreateAPIView):
    #TODO можно для безопасности потом добавить permission_classes = [IsAdminUser] - привилегия админа
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
