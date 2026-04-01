from rest_framework import serializers
from .models import Review
from product.models import Product
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'text', 'category', 'created_at']
