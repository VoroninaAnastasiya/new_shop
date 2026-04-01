from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from category.models import Category
from category.serializers import CategorySerializer


class CategoryAPIView(generics.ListCreateAPIView):
    """ API‑эндпоинт для работы с категориями товаров.

        Назначение:
        - возвращает список всех категорий (GET);
        - позволяет создавать новые категории (POST);
        - используется в административной части или при наполнении каталога."""
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoriesHTMLView(APIView):
    '''HTML‑представление списка категорий.

        Назначение:
        - выводит все категории в виде HTML‑страницы;
        - используется в пользовательском интерфейсе каталога;
        - рендерит шаблон categories_page.html.
    '''
    queryset = Category.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'categories_page.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return Response({'categories': categories})


class CategoryProductsHTMLView(APIView):
    '''HTML‑представление товаров одной категории'''
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'category_products_page.html'

    def get(self, request, pk):
        # Получаем категорию и сразу подтягиваем связанные товары
        category = (
            Category.objects
            .prefetch_related(
                'products__brand',        # подтянуть бренд товара
                'products__categories'    # подтянуть категории товара
            )
            .get(pk=pk)
        )

        # Товары уже подтянуты prefetch_related
        products = category.products.all()

        return Response({
            'category': category,
            'products': products
        })