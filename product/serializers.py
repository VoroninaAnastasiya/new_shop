from rest_framework import serializers

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для полной информации о товаре.
        Назначение:
        - используется для отображения товара в каталоге, карточке товара и API;
        - возвращает все ключевые поля модели Product, включая бренд, категории,
          изображение, цену, описание и даты создания/обновления;
        - подходит для списков товаров и детальных представлений.

        Особенности:
        - включает id, что важно для фронтенда и ссылок на товар;
        - ManyToManyField categories сериализуется как список id категорий;
        - ForeignKey brand сериализуется как id бренда;
        - image возвращается как URL, если настроен MEDIA_URL."""

    class Meta:
        model = Product
        fields = ('id','name', 'price', 'brand', 'description', 'available_quantity',
                  'categories', 'image', 'created_at', 'updated_at')#16.02 добавила id в fields


class ProductAvailabilitySerializer(serializers.ModelSerializer):
    """Упрощённый сериализатор для проверки наличия товара.
        - используется в эндпоинтах, где нужно вернуть только базовую информацию:
          id, название и количество доступного товара;"""

    class Meta:
        model = Product
        fields = ['id', 'name', 'available_quantity']