from rest_framework import serializers
from .models import CartItem
from product.models import Product

class ProductShortSerializer(serializers.ModelSerializer):
    #сериализатор для отображения краткой информации о товаре.
    #Показываем только нужные поля товара: id, name, price
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductShortSerializer(read_only=True)
    #Вложенный сериализатор: вместо product_id будет отображаться объект с id, name, price
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price', 'added_at']

    def get_total_price(self, obj): #obj - это экземпляр модели, которую сериализатор обрабатывает, объект CartItem
        #Метод, который вызывает get_total_price() из модели и возвращает сумму
        return obj.get_total_price()

    def create(self, validated_data):
        product = validated_data.pop('product_id')
        return CartItem.objects.create(product=product, **validated_data)