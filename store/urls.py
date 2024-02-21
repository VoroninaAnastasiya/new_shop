from django.urls import path

from .views import get_store_page, get_add_product_page

urlpatterns = [
    path('', get_store_page, name='home'),
    path('add_product/', get_add_product_page, name='add_product'),
]