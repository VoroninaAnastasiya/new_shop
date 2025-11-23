from django.urls import path

from .views import CategoryAPIView

urlpatterns = [
    path('list_category', CategoryAPIView.as_view(), name='categories'),
]