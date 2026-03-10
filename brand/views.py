from rest_framework import generics, filters
from rest_framework.permissions import IsAdminUser, AllowAny

from product.models import Product
from .models import Brand
from .serializers import BrandSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


class BrandsAPIView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'id']

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]


class BrandDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser]


class BrandsHTMLView(generics.ListAPIView):
    queryset = Brand.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'brands_page.html'

    def list(self, request, *args, **kwargs):
        return Response({'brands': self.get_queryset()})


class BrandProductsHTMLView(generics.ListAPIView):
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
        })

