from rest_framework import generics, permissions
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
    return render(request, 'test.jinja')


class MainPageHTMLAPIView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = []
    template_name = 'main_page.html'

    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        products = Product.objects.all()
        categories = Category.objects.all()
        brands = Brand.objects.all()

        return Response({
            'products': products,
            'categories': categories,
            'brands': brands,
        })


# Create your views here.
class ProductsAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination


class ProductCreateAPIView(generics.CreateAPIView):
    #TODO можно ограничить доступ - permission_classes = [IsAdminUser] - чтобы не все могли создавать товар
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductAvailabilityView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self,request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response ({'error': 'Товар не найден'}, status=404)

        return Response({
            'id': product.id,
            'name': product.name,
            'available_quantity': product.available_quantity
        })


class ProductDetailHTMLView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'product_detail.html'

    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        return Response({'product': product})