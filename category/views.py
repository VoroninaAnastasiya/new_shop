from django.shortcuts import render
from rest_framework import generics

from category.models import Category
from category.serializers import CategorySerializer


class CategoryAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
