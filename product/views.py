from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product
from product.serializers import ProductSerializer


# Create your views here.
class ProductsAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateAPIView(generics.CreateAPIView):
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