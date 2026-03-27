from django.shortcuts import render
import uuid
import json
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from yookassa import Configuration, Payment as YooPayment
from .models import Payment
from order.models import Order

# Вынеси в env
Configuration.account_id = 'ТВОЙ_SHOP_ID'
Configuration.secret_key = 'ТВОЙ_SECRET_KEY'


# ---------------------------------------------------------
# 1. ОПЛАТА ЧЕРЕЗ ЮKASSA
# ---------------------------------------------------------
def create_payment(request, order_id):
    '''Создаёт платёж в ЮKassa или использует существующий, если он уже есть.'''
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
                f"/payments/success/{order.id}/"
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
# 2. ОПЛАТА КАРТОЙ (твоя внутренняя логика)
# ---------------------------------------------------------
def pay_by_card(request, order_id):
    """Это текущая логика оплаты картой (не ЮKassa).
       Здесь мы просто считаем оплату успешной.
    """
    order = get_object_or_404(Order, id=order_id)

    payment_obj, created = Payment.objects.get_or_create(
        order=order,
        defaults={'method': 'card', 'status': 'pending'}
    )

    # Считаем, что карта оплачена успешно
    payment_obj.status = 'paid'
    payment_obj.save()

    order.status = 'paid'
    order.save()

    return redirect('payment_success', order_id=order.id)


# ---------------------------------------------------------
# 3. ОПЛАТА НАЛИЧНЫМИ
# ---------------------------------------------------------
def pay_cash(request, order_id):
    """Оплата наличными — статус остаётся pending."""
    order = get_object_or_404(Order, id=order_id)

    Payment.objects.get_or_create(
        order=order,
        defaults={'method': 'cash', 'status': 'pending'}
    )

    return redirect('payment_success', order_id=order.id)


# ---------------------------------------------------------
# 4. SUCCESS PAGE
# ---------------------------------------------------------
def payment_success(request, order_id):
    """Отображает страницу успешной оплаты."""
    order = get_object_or_404(Order, id=order_id)
    payment = getattr(order, 'payment', None)

    return render(request, 'success_page.html', {
        'order': order,
        'payment': payment,
    })


# ---------------------------------------------------------
# 5. FAIL PAGE
# ---------------------------------------------------------
def payment_fail(request, order_id):
    """Отображает страницу ошибки оплаты."""
    order = get_object_or_404(Order, id=order_id)
    payment = getattr(order, 'payment', None)

    return render(request, 'fail_page.html', {
        'order': order,
        'payment': payment,
    })


# ---------------------------------------------------------
# 6. WEBHOOK ЮKASSA
# ---------------------------------------------------------
def yookassa_webhook(request):
    """
        Обрабатывает webhook‑уведомления от ЮKassa.

        Назначение:
        - принимает POST‑запросы от ЮKassa о статусе платежа;
        - обновляет статус Payment и Order в зависимости от события;
        - обеспечивает корректную синхронизацию статусов.

        Логика:
        1. Прочитать JSON‑тело запроса.
        2. Извлечь event и object.
        3. Получить order_id из metadata.
        4. Найти заказ и платёж.
        5. Если event == 'payment.succeeded':
             - payment.status = 'paid'
             - order.status = 'paid'
        6. Если event == 'payment.canceled':
             - payment.status = 'canceled'
        7. Вернуть HTTP 200.

        Особенности:
        - webhook должен быть доступен публично;
        - ЮKassa ожидает статус 200, иначе будет повторять запросы;
        - metadata используется для связи платежа с заказом.
        """
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
