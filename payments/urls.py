from django.urls import path
from .views import (
    CreatePaymentView,
    PayByCardView,
    PayCashView,
    PaymentSuccessView,
    PaymentFailView,
    YookassaWebhookView,
)

urlpatterns = [
    path('create/<int:order_id>/', CreatePaymentView.as_view(), name='create_payment'),
    path('card/<int:order_id>/', PayByCardView.as_view(), name='pay_by_card'),
    path('cash/<int:order_id>/', PayCashView.as_view(), name='pay_cash'),

    path('success/<int:order_id>/', PaymentSuccessView.as_view(), name='payment_success'),
    path('fail/<int:order_id>/', PaymentFailView.as_view(), name='payment_fail'),

    path('webhook/yookassa/', YookassaWebhookView.as_view(), name='yookassa_webhook'),
]