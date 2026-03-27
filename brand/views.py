from rest_framework import generics, filters
from rest_framework.permissions import IsAdminUser, AllowAny

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

        Особенности:
        - TemplateHTMLRenderer возвращает HTML вместо JSON;
        - метод list() передаёт в шаблон QuerySet брендов;
        - может быть расширена поиском и сортировкой на стороне фронтенда.
        """
    queryset = Brand.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'brands_page.html'

    def list(self, request, *args, **kwargs):
        return Response({'brands': self.get_queryset()})


class BrandProductsHTMLView(generics.ListAPIView):
    """
        HTML‑вьюха для отображения товаров конкретного бренда.

        Назначение:
        - показывает все товары, относящиеся к выбранному бренду;
        - используется в каталоге для фильтрации товаров по бренду;
        - рендерит шаблон brand_products_page.html.

        Особенности:
        - get_queryset() фильтрует товары по brand_id;
        - list() передаёт в шаблон сам бренд и его товары;
        - TemplateHTMLRenderer возвращает HTML‑страницу.

        Использование:
        - /brands/<pk>/ — страница бренда;
        - отображает товары в виде карточек.
        """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'brand_products_page.html'

    def get_queryset(self):
        brand_id = self.kwargs['pk']
        return Product.objects.filter(brand_id=brand_id)

    def list(self, request, *args, **kwargs):
        brand = Brand.objects.get(pk=self.kwargs['pk'])
        products = self.get_queryset()
        return Response({
            'brand': brand,
            'products': products
        }) # в шаблон передаётся бренд и список товаров.