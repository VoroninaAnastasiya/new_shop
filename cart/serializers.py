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
        user = validated_data['user']
        quantity = validated_data.get('quantity', 1)

        # Проверка остатков
        if product.available_quantity < quantity:
            raise serializers.ValidationError('Недостаточно товара в наличии')

        # Если товар уже есть в корзине — увеличиваем количество
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            new_quantity = cart_item.quantity + quantity

            if product.available_quantity < new_quantity:
                raise serializers.ValidationError('Недостаточно товара в наличии')

            # и сохраняем только если количество реально изменилось
            if cart_item.quantity != new_quantity:
                cart_item.quantity = new_quantity
                cart_item.save()

        return cart_item

    def update(self, instance, validated_data):
        # Проверка при изменении количества
        quantity = validated_data.get('quantity', instance.quantity)
        if instance.product.available_quantity < quantity:
            raise serializers.ValidationError("Недостаточно товара в наличии")
        instance.quantity = quantity
        instance.save()
        return instance