from django.urls import path

from .views import ProductsAPIView, ProductCreateAPIView, ProductAvailabilityView, MainPageHTMLAPIView, test, \
    ProductDetailHTMLView

urlpatterns = [
    path('list_products/', ProductsAPIView.as_view()),
    path('create_product/', ProductCreateAPIView.as_view()),
    path('<int:pk>/availability/', ProductAvailabilityView.as_view(), name='product-availability'),

    path('<int:pk>/', ProductDetailHTMLView.as_view(), name='product_detail_page'),
    path('test/', test, name='test_page'),
]
