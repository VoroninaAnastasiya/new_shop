from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    # как вариант можно вместо предыдущей записи сделать так - def get_queryset(self):
    # return Order.objects.filter(user=self.request.user) - чужие записи не будут видны
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_from_cart(self, request):
        user = request.user
        cart_items = user.cart_items.all()

        if not cart_items.exists():
            return Response({'error': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка остатков товара
        for cart_item in cart_items:
            if cart_item.product.available_quantity < cart_item.quantity:
                return Response( {'error': f"Недостаточно товара: {cart_item.product.name}"},
                                 status=status.HTTP_400_BAD_REQUEST )

        delivery_type = request.data.get('delivery_type')
        delivery_data = request.data.get('delivery_data')
        delivery_time = request.data.get('delivery_time')

        if delivery_type == 'pickup':
            if delivery_time is not None or delivery_data is not None:
                return Response(
                    {'error': 'delivery_time и delivery_data должны быть пустыми'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        order = Order.objects.create(
            user=user,
            city=request.data.get('city'),
            address=request.data.get('address'),
            payment_type=request.data.get('payment_type'),
            delivery_type=delivery_type,
            delivery_data=delivery_data,
            delivery_time=delivery_time,
            comment=request.data.get('comment'),
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
            #списание остатков
            cart_item.product.available_quantity -= cart_item.quantity
            cart_item.product.save()
        cart_items.delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)