from rest_framework import serializers

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name', 'price', 'brand', 'description', 'available_quantity',
                  'categories', 'image', 'created_at', 'updated_at')#16.02 добавила id в fields


class ProductAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'available_quantity']
