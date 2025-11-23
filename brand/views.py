from rest_framework import generics

from .models import Brand
from .serializers import BrandSerializer


class BrandsAPIView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
