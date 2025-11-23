from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CartItem
from .serializers import CartItemSerializer

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        #метод для ограничения доступа: каждый пользователь видит только свои товары в корзине
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # метод, отвечающий за создание нового CartItem, автоматически подставляя текущего пользователя
        serializer.save(user=self.request.user)


class CartTotalView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = CartItem.objects.filter(user=request.user)
        total = sum([item.get_total_price() for item in items]) #item.get_total_price() —
        # метод модели, возвращающий price * quantity
        return  Response({'total_price': total})