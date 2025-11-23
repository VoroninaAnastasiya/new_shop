from django.urls import path

from product.views import ProductsAPIView, ProductCreateAPIView

urlpatterns = [
    path('list_products', ProductsAPIView.as_view()),
    path('create_product', ProductCreateAPIView.as_view()),
]