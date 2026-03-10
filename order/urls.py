from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderHTMLAPIView, payment_page, success_page, OrderDetailHTMLView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
# router.register(r'order_page', OrderViewSet, basename='order_page')

urlpatterns = [ path('', OrderHTMLAPIView.as_view(), name='orders_page'),
                path('payment/<int:order_id>/', payment_page, name='payment_page'),
                path('success/<int:order_id>/', success_page, name='success_page'),
                path('<int:pk>/', OrderDetailHTMLView.as_view(), name='order_detail_page'),
                ]

urlpatterns += router.urls