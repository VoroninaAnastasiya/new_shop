from rest_framework import generics, permissions
from rest_framework.permissions import IsAdminUser
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render, get_object_or_404

from brand.models import Brand
from category.models import Category
from product.models import Product
from product.serializers import ProductSerializer

from .pagination import ProductPagination
def test(request):
    """Вспомогательная функция для рендера тестового шаблона."""
    return render(request, 'test.jinja')


class MainPageHTMLAPIView(generics.ListAPIView):
    """ Для отображения главной страницы каталога.

        Назначение:
        - выводит список товаров, категорий и брендов;
        - используется для основной витрины магазина;

        Особенности:
        - TemplateHTMLRenderer рендерит HTML вместо JSON;
        - queryset определён, но метод get переопределён для передачи
          дополнительных данных (категории и бренды);
        - данные передаются в шаблон в виде QuerySet’ов.

        Использование:
        - отображение главной страницы каталога;
        - может быть расширена фильтрацией, поиском, сортировкой.
        """

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main_page.html'

    queryset = Product.objects.all()

    def get(self, request, *args, **kwargs):
        """Возвращает HTML‑страницу с товарами, категориями и брендами."""
        products = Product.objects.all()
        categories = Category.objects.all()
        brands = Brand.objects.all()

        return Response({
            'products': products,
            'categories': categories,
            'brands': brands,
        })


class ProductsAPIView(generics.ListAPIView):
    """API‑эндпоинт для получения списка товаров.

        Назначение:
        - возвращает список товаров в формате JSON;
        - поддерживает пагинацию через ProductPagination;
        - используется для фронтенда, AJAX‑запросов и мобильных приложений.

        Особенности:
        - ProductSerializer возвращает полную информацию о товаре;
        - ProductPagination ограничивает размер страницы."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


class ProductCreateAPIView(generics.CreateAPIView):
    """API‑эндпоинт для создания нового товара.
        Назначение:
        - принимает данные товара и создаёт запись в базе;
        - используется для административной части проекта.
        """
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductAvailabilityView(APIView):
    """API‑эндпоинт для проверки количества товара в наличии.
        Назначение:
        - возвращает id, название и количество доступного товара;
        - используется корзиной, оформлением заказа"""
    permission_classes = [permissions.AllowAny]

    def get(self,request, pk):
        """Возвращает информацию о наличии товара."""
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response ({'error': 'Товар не найден'}, status=404)

        return Response({
            'id': product.id,
            'name': product.name,
            'available_quantity': product.available_quantity
        })#TODO get_object_or_404 django product = get_object_or_404(Product, id=pk)


class ProductDetailHTMLView(APIView):
    """Класс для отображения карточки товара в HTML.
        Назначение: показывает подробную информацию о товаре, используется в веб‑интерфейсе магазина,
        рендерит шаблон product_detail.html."""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'product_detail.html'

    def get(self, request, pk):
        """Возвращает HTML‑страницу с данными товара."""
        product = get_object_or_404(Product, id=pk)
        return Response({'product': product})


class HomePageView(APIView):
    """Класс для отображения домашней страницы сайта"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'home_page.html'

    def get(self, request):
        """Возвращает пустой контекст для шаблона."""
        return Response({})


class ProductsPageView(APIView):
    """Класс для отображения страницы каталога товаров.
        Назначение:
        - выводит список товаров, категорий и брендов;
        - используется для полноценной HTML‑страницы каталога;
        - рендерит шаблон products_page.html.
        """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'products_page.html'

    def get(self, request):
        """Возвращает HTML‑страницу каталога"""
        categories = Category.objects.all()
        brands = Brand.objects.all()
        products = Product.objects.all()
        return Response({
            'categories': categories,
            'brands': brands,
            'products': products
        })