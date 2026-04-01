from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    OrderViewSet,
    OrderHTMLAPIView,
    OrderDetailHTMLView,
    PaymentPageView,
    SuccessPageView,
)

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    # HTML список заказов
    path('', OrderHTMLAPIView.as_view(), name='orders_page'),

    # HTML страница оплаты заказа
    path('orders/payment/<int:order_id>/', PaymentPageView.as_view(), name='payment_page'),

    # HTML success после оплаты
    path('orders/success/<int:order_id>/', SuccessPageView.as_view(), name='success_page'),

    # HTML страница одного заказа
    path('<int:pk>/', OrderDetailHTMLView.as_view(), name='order_detail_page'),
]

urlpatterns += router.urls
