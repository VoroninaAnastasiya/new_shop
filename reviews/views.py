from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from .models import Review


class ReviewsHTMLView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [AllowAny]
    template_name = 'reviews_page.html'

    def get(self, request):
        reviews = Review.objects.all().order_by('-created_at')
        return Response({'reviews': reviews})

