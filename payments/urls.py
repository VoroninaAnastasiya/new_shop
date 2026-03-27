from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:order_id>/', views.create_payment, name='create_payment'),
    path('card/<int:order_id>/', views.pay_by_card, name='pay_by_card'),
    path('cash/<int:order_id>/', views.pay_cash, name='pay_cash'),
    path('success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('fail/<int:order_id>/', views.payment_fail, name='payment_fail'),
    path('webhook/yookassa/', views.yookassa_webhook, name='yookassa_webhook'),
]
