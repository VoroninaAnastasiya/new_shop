from django.core.mail import EmailMessage

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
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
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        # здесь можно добавить логику оплаты
        return redirect('success_page', order_id=order.id)

    return render(request, 'payment.html', {'order': order})


@login_required
def success_page(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'success.html', {'order': order})


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    # как вариант можно вместо предыдущей записи сделать так - def get_queryset(self):
    # return Order.objects.filter(user=self.request.user) - чужие записи не будут видны
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_from_cart(self, request):
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

        print("delivery_type:", delivery_type)
        print("delivery_time:", repr(delivery_time))
        print("delivery_data:", repr(delivery_data))

        if delivery_type == 'pickup':
            if delivery_type == 'pickup':
                delivery_time = None
                delivery_data = None

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

        #     'Тестовое письмо',
        #     'Поздравляем! Ваш заказ оформлен',
        #     settings.EMAIL_HOST_USER,
        #     ['voronina-nastya.97@yandex.ru'],
        #     fail_silently=False,
        # )
        #! rabbitmq отправка на почту html о созданном заказе. rabbitmq подключение,
        # потом в отдельном файле делаешь функцию которая будет отправлять сообщение на почту.
        # Пример rabbitmq в checkin-core проекте
        # exchange = Exchange(settings.UPDATER_V2['EXCHANGE_TO_UPDATER_V2'], type='topic')
        # pusher = RabbitMQPusher()
        #
        # entry_form_data = {
        #     "url": "/documents/",
        #     "method": "POST",
        #     "changes": input_data
        # }
        # pusher.send(entry_form_data, exchange, routing_key)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def send_order_email(order):
    service = JinjaEmailService(
        template_name='emails/order_success.jinja',
        context={'order': order, 'user': order.user},
        to_email='voronina-nastya.97@yandex.ru', # тест
    )
    service.send(f'Ваш заказ №{order.id} успешно оформлен')


class OrderHTMLAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated]
    template_name = 'orders.html'

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        return Response({'orders': orders})


class OrderDetailHTMLView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'order_detail.html'
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        items = order.items.select_related('product')
        return Response({'order': order, 'items': items})

