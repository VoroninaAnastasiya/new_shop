from rest_framework import serializers

from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Category.

        Назначение:
        - возвращает данные категории в формате JSON;
        - используется в API‑эндпоинтах для списка и создания категорий;
        - обеспечивает передачу id, названия и временных меток.

        Поля:
        - id — уникальный идентификатор категории (добавлен для удобства фронтенда);
        - name — название категории;
        - created_at — дата создания записи;
        - updated_at — дата последнего обновления.

        Особенности:
        - сериализатор минималистичен и подходит для большинства CRUD‑операций;
        - используется в CategoryAPIView и других API‑вьюхах.
        """
    class Meta:
        model = Category
        fields = ('id', 'name', 'created_at', 'updated_at') #TODO 16.02 добавлено поле id