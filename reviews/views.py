from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from .models import Review
from .serializers import ReviewSerializer


class ReviewsHTMLView(APIView):
    """
        Класс для отображения страницы HTML с отзывами.

        Назначение:
        - выводит список всех отзывов, оставленных пользователями;
        - используется для обычного веб‑интерфейса (не API);
        - отображает данные через HTML‑шаблон reviews_page.html.

        Особенности:
        - TemplateHTMLRenderer возвращает HTML, а не JSON;
        - AllowAny — страница доступна всем пользователям, в том числе неавторизованным;
        - отзывы сортируются по дате создания (новые сверху);
        - в шаблон передаётся QuerySet отзывов, который можно отрисовать в виде карточек.

        Использование:
        - применяется для публичной страницы отзывов;
        - удобно для SEO и для демонстрации клиентам реального опыта других людей.
        """
    renderer_classes = [TemplateHTMLRenderer]
    #permission_classes = [AllowAny]
    template_name = 'reviews_page.html'

    def get(self, request):
        """Возвращает HTML‑страницу со списком отзывов."""
        reviews = Review.objects.all().order_by('-created_at')
        return Response({'reviews': reviews})

class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]


class ReviewSubmitHTMLView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'review_form.html'
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({})

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('reviews_page')
        return Response({'errors': serializer.errors})



