from django.urls import path

from .views import ProductsAPIView, ProductCreateAPIView, ProductAvailabilityView, MainPageHTMLAPIView, test

urlpatterns = [
    path('list_products/', ProductsAPIView.as_view()),
    path('create_product/', ProductCreateAPIView.as_view()),
    path('<int:pk>/availability/', ProductAvailabilityView.as_view(), name='product-availability'),
    path('', MainPageHTMLAPIView.as_view(), name='products_page'),
    path('test/', test, name='test_page'),
]
