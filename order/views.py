from user_auth.models import User
from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from documents.views import JinjaEmailService
from .models import Order, OrderItem
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order

@login_required
def payment_page(request, order_id):
    """ HTML‑страница оплаты заказа.

        Назначение:
        - отображает страницу оплаты для конкретного заказа;
        - доступна только авторизованным пользователям;
        - используется для ручной/внутренней логики оплаты.

        Логика:
        1. Получить заказ текущего пользователя.
        2. Если POST — выполнить оплату (логика может быть расширена).
        3. Если GET — отобразить шаблон payment.html с данными заказа.
        """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        # здесь можно добавить логику оплаты
        return redirect('success_page', order_id=order.id)

    return render(request, 'payment.html', {'order': order})


@login_required
def success_page(request, order_id):
    """ HTML‑страница успешной оплаты.

        Назначение:
        - отображает подтверждение успешной оплаты;
        - показывает данные заказа пользователю.

        Логика:
        1. Получить заказ текущего пользователя.
        2. Передать его в шаблон success.html.
        """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'success.html', {'order': order})


class OrderViewSet(viewsets.ModelViewSet):
    """ API‑вьюсет для работы с заказами.
        Назначение:
        - предоставляет CRUD‑операции для модели Order;
        - использует OrderSerializer для отображения данных;
        - доступен только авторизованным пользователям."""
    queryset = Order.objects.all()
    # как вариант можно вместо предыдущей записи сделать так - def get_queryset(self):
    # return Order.objects.filter(user=self.request.user) - чужие записи не будут видны
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_from_cart(self, request):
        """Создаёт заказ на основе корзины пользователя."""
        user = User.objects.get(id=request.user.id)
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
            if any([delivery_time, delivery_data]):
                return Response({'error': 'нельзя указывать delivery_time и delivery_data'},
                                status=status.HTTP_400_BAD_REQUEST)

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
        # мне пиздец, надо через bulk_create для OrderItem
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )

            #списываем то же в цикле...подумать как, мб через bulk_...
            cart_item.product.available_quantity -= cart_item.quantity
            cart_item.product.save()

        # Пересчёт суммы
        order.total_price = sum(item.product.price * item.quantity for item in order.items.all())
        order.save()

        cart_items.delete()
        # Отправка письма
        JinjaEmailService( template_name='test.jinja',
                           context={'user': user, 'order': order},
                           to_email='voronina-nastya.97@yandex.ru'
        ).send('Ваш заказ оформлен')
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def send_order_email(order):
    """ Отправляет письмо пользователю о том, что заказ успешно оформлен."""
    service = JinjaEmailService(
        template_name='emails/order_success.jinja',
        context={'order': order, 'user': order.user},
        to_email='voronina-nastya.97@yandex.ru', # тест
    )
    service.send(f'Ваш заказ №{order.id} успешно оформлен')


class OrderHTMLAPIView(APIView):
    """ HTML‑вьюха для отображения списка заказов пользователя.
        Назначение:
        - показывает все заказы текущего пользователя;
        - используется в личном кабинете;
        - рендерит шаблон orders.html.
        Особенности:
        - доступна только авторизованным пользователям.
        """
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated]
    template_name = 'orders.html'

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return Response({'orders': orders})


class OrderDetailHTMLView(APIView):
    """Класс для отображения деталей конкретного заказа."""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'order_detail.html'
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        items = order.items.select_related('product')
        return Response({'order': order, 'items': items})