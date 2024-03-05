from django.urls import path

from .views import get_store_page, get_add_product_page, get_all_lichi_products, get_all_zara_products, register, \
    auth_login

urlpatterns = [
    path('', get_store_page, name='home'),
    path('add_product/', get_add_product_page, name='add_product'),
    path('Lichi/<int:id>/', get_all_lichi_products, name='lichi'),
    path('Zara/', get_all_zara_products, name='zara'),
    path('register/', register, name='register'),
    path('auth/', auth_login, name='login'),
]