from django.urls import path

from product.views import ProductsAPIView, ProductCreateAPIView, ProductAvailabilityView

urlpatterns = [
    path('list_products', ProductsAPIView.as_view()),
    path('create_product', ProductCreateAPIView.as_view()),
    path('<int:pk>/availability/', ProductAvailabilityView.as_view(), name='product-availability'),
]
