from rest_framework import serializers
from .models import CartItem
from product.models import Product

class ProductShortSerializer(serializers.ModelSerializer):
    """ Краткий сериализатор товара.

    Назначение:
    - используется внутри CartItemSerializer для отображения товара
      в компактном виде;
    - возвращает только ключевые поля: id, name, price;
    - уменьшает объём данных в ответе и ускоряет работу API."""
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    """Сериализатор позиции корзины (CartItem).
       Вложенный сериализатор: вместо product_id будет отображаться объект с id, name, price.
       Показывает товар в виде вложенного объекта. Принимает product_id при создании. Возвращает total_price.

       Назначение:
    - отображает товар как вложенный объект (ProductShortSerializer);
    - принимает product_id при создании позиции;
    - возвращает total_price позиции;
    - выполняет проверку остатков товара при создании и обновлении."""
    product = ProductShortSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price', 'added_at']

    def get_total_price(self, obj): #obj - это экземпляр модели, которую сериализатор обрабатывает, объект CartItem
        '''Возвращает итоговую стоимость позиции. Метод, который вызывает get_total_price() из модели и возвращает сумму'''
        return obj.get_total_price()

    def create(self, validated_data):
        '''Создаёт или обновляет позицию корзины.

           Метод для проверки остатков товара. Если товар уже есть в корзине — увеличивает количество.
           Если количество превышает остаток — ошибка.

           Логика:
        1. Получить product и user.
        2. Проверить, хватает ли товара на складе.
        3. Найти или создать CartItem.
        4. Если позиция уже существует — увеличить количество.
        5. Проверить остатки повторно.
        6. Сохранить изменения.'''

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
        """Обновляет количество товара в позиции корзины.

        Назначение:
        - проверяет остатки перед изменением количества;
        - предотвращает установку количества, превышающего доступное.

        Логика:
        1. Получить новое количество.
        2. Проверить остатки.
        3. Сохранить изменения.
        """
        quantity = validated_data.get('quantity', instance.quantity)
        if instance.product.available_quantity < quantity:
            raise serializers.ValidationError("Недостаточно товара в наличии")
        instance.quantity = quantity
        instance.save()
        return instance