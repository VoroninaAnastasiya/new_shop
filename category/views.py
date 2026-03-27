from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from category.models import Category
from category.serializers import CategorySerializer
from product.models import Product


class CategoryAPIView(generics.ListCreateAPIView):
    """ API‑эндпоинт для работы с категориями товаров.

        Назначение:
        - возвращает список всех категорий (GET);
        - позволяет создавать новые категории (POST);
        - используется в административной части или при наполнении каталога."""
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoriesHTMLView(generics.ListAPIView):
    '''HTML‑представление списка категорий.

        Назначение:
        - выводит все категории в виде HTML‑страницы;
        - используется в пользовательском интерфейсе каталога;
        - рендерит шаблон categories_page.html.
    '''
    queryset = Category.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'categories_page.html'
    #TODO убмраем list, он не нужен так как мы и так выводим список
    def list(self, request, *args, **kwargs):
        return Response({'categories': self.get_queryset()})


class CategoryProductsHTMLView(generics.ListAPIView):
    '''HTML‑представление товаров одной категории'''
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'category_products_page.html'

    def get_queryset(self):
        category_id = self.kwargs['pk']
        return Product.objects.filter(categories__id=category_id)

    def list(self, request, *args, **kwargs):
        category = Category.objects.get(pk=self.kwargs['pk'])# как сделать одним запросом!
        products = self.get_queryset()
        return Response({
            'category': category,
            'products': products
        })