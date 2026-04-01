from django.urls import path, include
from rest_framework.routers import DefaultRouter


from user.urls import urlpatterns
from .views import CartHTMLDetailView, CartItemViewSet, CartTotalView, checkout, AddToCartView

router = DefaultRouter()
router.register(r'cart-items', CartItemViewSet, basename='cart')

urlpatterns = [
    path('', CartHTMLDetailView.as_view(), name='cart_page'),
    path('total/', CartTotalView.as_view(), name='cart_total'),
    path('checkout/', checkout, name='checkout_page'),
    path('add/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
]

urlpatterns += router.urls