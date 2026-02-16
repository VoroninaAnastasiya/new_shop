from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'items', 'total_price']


# {"delivery":{"id":447,"cityId":54147,"shopId":376537,"date":null},"payment":{"groupId":1,"id":"510","creditActivityId":null,"legalEntity":null,"save":false},"personal":{"name":"рсарсрпр","phone":"375295656412"},"comment":"","coupon":null,"spendBonuses":null,"save":false,"code":"","isBonusesUsed":false}