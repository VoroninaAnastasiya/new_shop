import json
import uuid
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from yookassa import Payment as YooPayment

from order.models import Order
from .models import Payment


# ---------------------------------------------------------
# 1. ОПЛАТА ЧЕРЕЗ ЮKASSA
# ---------------------------------------------------------
class CreatePaymentView(APIView):
    """
    Создаёт платёж в ЮKassa или использует существующий.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        payment_obj, created = Payment.objects.get_or_create(
            order=order,
            defaults={'method': 'yookassa', 'status': 'pending'}
        )

        yoo_payment = YooPayment.create({
            "amount": {
                "value": str(order.total_price),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": request.build_absolute_uri(
                    reverse('payment_success', args=[order.id])
                ),
            },
            "capture": True,
            "description": f"Заказ №{order.id}",
            "metadata": {
                "order_id": order.id
            }
        }, uuid.uuid4())

        payment_obj.payment_id = yoo_payment.id
        payment_obj.save()

        return redirect(yoo_payment.confirmation.confirmation_url)


# ---------------------------------------------------------
# 2. ОПЛАТА КАРТОЙ (внутренняя логика)
# ---------------------------------------------------------
class PayByCardView(APIView):
    """
    Внутренняя логика оплаты картой (не ЮKassa).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        payment_obj, created = Payment.objects.get_or_create(
            order=order,
            defaults={'method': 'card', 'status': 'pending'}
        )

        payment_obj.status = 'paid'
        payment_obj.save()

        order.status = 'paid'
        order.save()

        return redirect('payment_success', order_id=order.id)


# ---------------------------------------------------------
# 3. ОПЛАТА НАЛИЧНЫМИ
# ---------------------------------------------------------
class PayCashView(APIView):
    """
    Оплата наличными — статус остаётся pending.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        Payment.objects.get_or_create(
            order=order,
            defaults={'method': 'cash', 'status': 'pending'}
        )

        return redirect('payment_success', order_id=order.id)


# ---------------------------------------------------------
# 4. SUCCESS PAGE
# ---------------------------------------------------------
class PaymentSuccessView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'success_page.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        payment = getattr(order, 'payment', None)

        return Response({
            'order': order,
            'payment': payment
        })


# ---------------------------------------------------------
# 5. FAIL PAGE
# ---------------------------------------------------------
class PaymentFailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'fail_page.html'

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        payment = getattr(order, 'payment', None)

        return Response({
            'order': order,
            'payment': payment
        })


# ---------------------------------------------------------
# 6. WEBHOOK ЮKASSA
# ---------------------------------------------------------
class YookassaWebhookView(APIView):
    """
    Обрабатывает webhook‑уведомления от ЮKassa.
    """

    authentication_classes = []  # webhook должен быть публичным
    permission_classes = []      # ЮKassa не умеет авторизацию

    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        event = data.get('event')
        obj = data.get('object', {})

        order_id = obj.get('metadata', {}).get('order_id')
        if not order_id:
            return HttpResponse(status=400)

        order = Order.objects.get(id=order_id)
        payment = Payment.objects.get(order=order)

        if event == 'payment.succeeded':
            payment.status = 'paid'
            payment.save()

            order.status = 'paid'
            order.save()

        elif event == 'payment.canceled':
            payment.status = 'canceled'
            payment.save()

        return HttpResponse(status=200)
