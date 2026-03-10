"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from brand.views import BrandsHTMLView, BrandProductsHTMLView
from cart.views import CartHTMLDetailView
from order.views import OrderHTMLAPIView
from product.views import MainPageHTMLAPIView, HomePageView, ProductsPageView, ProductDetailHTMLView
from user.views import ProfileHTMLAPIView
from user_auth.views import LoginHTMLView, LogoutHTMLView, RegistrationHTMLView
from utils.views import test_rabbit, test_rabbit_reciver

schema_view = get_schema_view(
    openapi.Info(
        title="E-commerce API",
        default_version='v1',
        description="Документация API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Главная страница
    path('', HomePageView.as_view(), name='home_page'),

    # Товары
    path('products/', ProductsPageView.as_view(), name='products_page'),
    path('products/<int:pk>/', ProductDetailHTMLView.as_view(), name='product_detail_page'),

    # Категории и бренды
    path('categories/', include('category.urls')),
    path('brands/', BrandsHTMLView.as_view(), name='brands_page'),
    path('brands/<int:pk>/', BrandProductsHTMLView.as_view(), name='brand_products_page'),

    # Корзина
    path('cart/', include('cart.urls')),

    # Отзывы
    path('reviews/', include('reviews.urls')),

    # Заказы
    path('orders/', OrderHTMLAPIView.as_view(), name='orders_page'),
    path('orders/', include('order.urls')),  # API

    # Профиль
    path('profile/', ProfileHTMLAPIView.as_view(), name='profile_page'),

    # Аутентификация
    path('login/', LoginHTMLView.as_view(), name='login_page'),
    path('logout/', LogoutHTMLView.as_view(), name='logout_page'),
    path('register/', RegistrationHTMLView.as_view(), name='register_page'),
    # path('products/', ProductsPageView.as_view(), name='products_page'),

    # API
    path('api/', include('user_auth.urls', namespace='authentication')),
    path('api/products/', include('product.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('order.urls')),

    # Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

