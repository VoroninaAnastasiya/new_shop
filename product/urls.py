from django.urls import path

from .views import ProductsAPIView, ProductCreateAPIView, ProductAvailabilityView, MainPageHTMLAPIView, test, \
    ProductDetailHTMLView, HomePageView, ProductsPageView

urlpatterns = [
    path('list_products/', ProductsAPIView.as_view()),
    path('create_product/', ProductCreateAPIView.as_view()),
    path('<int:pk>/availability/', ProductAvailabilityView.as_view(), name='product-availability'),

    path('<int:pk>/', ProductDetailHTMLView.as_view(), name='product_detail_page'),
    path('test/', test, name='test_page'),
    path('', HomePageView.as_view(), name='home_page'),


    # Каталог товаров
    path('products/', ProductsPageView.as_view(), name='products_page'),

    # Детальная страница товара
    path('products/<int:pk>/', ProductDetailHTMLView.as_view(), name='product_detail_page'),

    # Старая главная (оставляем как отдельную страницу)
    path('main/', MainPageHTMLAPIView.as_view(), name='main_page_old'),
]

