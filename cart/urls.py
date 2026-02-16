from django.urls import path, include
from rest_framework.routers import DefaultRouter


from user.urls import urlpatterns
from .views import CartItemViewSet, CartTotalView

router = DefaultRouter()
router.register(r'cart-items', CartItemViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
    path('cart/total/', CartTotalView.as_view(), name='cart_total')
]