from django.urls import path

from documents.views import TestEmailAPIView

urlpatterns = [
    path('test-email/', TestEmailAPIView.as_view(), name='test_email'),
]