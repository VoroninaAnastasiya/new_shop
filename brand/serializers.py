from rest_framework import serializers

from brand.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Brand.

        Назначение:
        - используется для отображения и создания брендов через API;
        - возвращает все поля модели Brand, включая id, название, изображение
          и временные метки;
        - обеспечивает валидацию уникальности названия бренда.

        Поля:
        - id — идентификатор бренда;
        - name — название бренда (уникальное);
        - image — изображение бренда (логотип);
        - created_at — дата создания;
        - updated_at — дата последнего обновления.

        Особенности:
        - fields='__all__' делает сериализатор универсальным;
        - validate_name выполняет регистронезависимую проверку уникальности:
            * 'Adidas' и 'adidas' считаются одинаковыми;
        - используется в CategoryAPIView, BrandAPIView, HTML‑вьюхах и административных API.

        Валидация:
        - validate_name(value):
            Проверяет, существует ли бренд с таким же названием (без учёта регистра).
            Если существует — выбрасывает ValidationError.
        """
    class Meta:
        model = Brand
        fields = '__all__'

    def validate_name(self, value):
        if Brand.objects.filter(name__iexact=value).exists(): #Проверка: существует ли бренд с таким же названием.
            # iexact - чтобы сравнение было регистронезависимым: Adidas" и "adidas" считаются одинаковыми.
            raise serializers.ValidationError("Такой бренд уже существует.")
        return value