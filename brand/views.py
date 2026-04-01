from rest_framework import generics, filters
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


from product.models import Product
from .models import Brand
from .serializers import BrandSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


class BrandsAPIView(generics.ListCreateAPIView):
    """ API‑эндпоинт для работы с брендами.

        Назначение:
        - возвращает список всех брендов (GET);
        - позволяет создавать новые бренды (POST);
        - используется в административной части и при наполнении каталога.

        Поля и фильтры:
        - search_fields = ['name']:
            позволяет искать бренды по названию (регистронезависимо);
        - ordering_fields = ['name', 'id']:
            позволяет сортировать бренды по названию или id.

        Права доступа:
        - GET — доступен всем пользователям (AllowAny);
        - POST — только администраторам (IsAdminUser).

        Особенности:
        - BrandSerializer выполняет валидацию уникальности названия;
        - фильтрация и сортировка работают автоматически через DRF FilterBackend;
        - используется для API, а не для HTML‑интерфейса.
        """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name'] #позволяет искать бренды по названию
    ordering_fields = ['name', 'id'] #позволяет сортировать

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]


class BrandDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ API‑эндпоинт для работы с конкретным брендом.

        Назначение:
        - позволяет получить бренд по id (GET);
        - обновить данные бренда (PUT/PATCH);
        - удалить бренд (DELETE).

        Права доступа:
        - только администраторы (IsAdminUser).

        Особенности:
        - используется BrandSerializer;
        - подходит для административной панели или внутреннего API.
        """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser]


class BrandsHTMLView(generics.ListAPIView):
    """
        HTML‑вьюха для отображения списка брендов.

        Назначение:
        - выводит все бренды в виде HTML‑страницы;
        - используется в пользовательском интерфейсе каталога;
        - рендерит шаблон brands_page.html.

        """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'brands_page.html'
    queryset = Brand.objects.all()

    def get(self, request, *args, **kwargs):
        brands = self.get_queryset()
        return Response({'brands': brands})


class BrandProductsHTMLView(APIView):
    """
    HTML‑вьюха для отображения товаров конкретного бренда.

    Назначение:
    - показывает все товары выбранного бренда;
    - используется в каталоге для фильтрации по бренду;
    - рендерит шаблон brand_products_page.html.

    Особенности:
    - загружает бренд и связанные товары;
    - оптимизирована через select_related и prefetch_related;
    - возвращает HTML‑страницу через TemplateHTMLRenderer.
    """

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'brand_products_page.html'

    def get(self, request, pk):
        brand = get_object_or_404(Brand, pk=pk)

        products = (
            Product.objects
            .filter(brand_id=pk)
            .select_related('brand')
            .prefetch_related('categories')
        )

        return Response({
            'brand': brand,
            'products': products
        })
