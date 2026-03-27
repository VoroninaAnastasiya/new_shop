from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    '''Сериализатор OrderItemSerializer отдаёт товар и его количество.

    Назначение:
    - возвращает информацию о товаре и его количестве в составе заказа;
    - используется внутри OrderSerializer как вложенный сериализатор;
    - обеспечивает компактное представление позиции без лишних данных.
    '''
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор заказа (Order).

        Назначение:
        - возвращает полную информацию о заказе для API;
        - включает вложенные позиции заказа (items);
        - отображает пользователя в виде строки (email или username);
        - предоставляет итоговую сумму заказа.

        Поля:
        - id — идентификатор заказа;
        - user — строковое представление пользователя (StringRelatedField);
        - status — текущий статус заказа;
        - created_at — дата создания;
        - items — вложенный список позиций заказа (OrderItemSerializer);
        - total_price — итоговая сумма заказа.

        Особенности:
        - user — read_only, чтобы клиент не мог изменить владельца заказа;
        - items — read_only, так как позиции создаются через бизнес‑логику (viewset);
        - total_price — read_only, пересчитывается на стороне сервера;
        - сериализатор используется для отображения заказа после оформления,
          а также в списках заказов пользователя.
        """
    user = serializers.StringRelatedField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'items', 'total_price']