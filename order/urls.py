from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderHTMLAPIView

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order_page', OrderViewSet, basename='order_page')


urlpatterns = router.urls