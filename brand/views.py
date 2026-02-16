from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import Brand
from .serializers import BrandSerializer


class BrandsAPIView(generics.ListCreateAPIView):
    #TODO permission_classes = [IsAdminUser] - привилегия админа
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
