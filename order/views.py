from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_from_cart(self, request):
        user = request.user
        cart_items= user.cart_items.all()
        if not cart_items.exists():
            return Response({'error': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            user=user,
            city=request.data.get('city'),
            address=request.data.get('address'),
            payment_type=request.data.get('payment_type'),
            delivery_type=request.data.get('delivery_type'),
            delivery_date=request.data.get('delivery_date'),
            delivery_time=request.data.get('delivery_time'),
            comment=request.data.get('comment'),
        )

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
        cart_items.delete()
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)