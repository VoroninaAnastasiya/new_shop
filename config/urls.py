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

from cart.views import CartHTMLDetailView
from product.views import MainPageHTMLAPIView
from user.views import ProfileHTMLAPIView
from user_auth.views import LoginHTMLView, LogoutHTMLView, RegistrationHTMLView

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
    path('products/', include('product.urls',)),
    #Главная страница
    path('', MainPageHTMLAPIView.as_view(), name='main_page'),
    path('brands/', include('brand.urls'), name='Бренды'),
    #path('users/', include('user.urls'), name='Пользователи'),
    #path('user/', include('user.urls')),
    path('categories/', include('category.urls'), name='Категории товаров'),
    path('cart/', include('cart.urls')),
    path('documents/', include('documents.urls')),

    path('login/', LoginHTMLView.as_view(), name='login_page'),
    path('logout/', LogoutHTMLView.as_view(), name='logout_page'),
    path('register/', RegistrationHTMLView.as_view(), name='register_page'),
    path('profile/', ProfileHTMLAPIView.as_view(),name='profile_page'),

    path('person_cart/', CartHTMLDetailView.as_view(), name='cart_page'),
    #path('login/', ProfileHTMLAPIView.as_view(), name='profile_page'),
# API
    path('api/', include('user_auth.urls', namespace='authentication')),
    path('api/products/', include('product.urls'), name='Товары'),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('order.urls')),
# JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # логин
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # обновление
# Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

