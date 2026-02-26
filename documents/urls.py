from django.urls import path

from documents.views import test_email
urlpatterns = [
    path('test-email/', test_email, name='test_email'),
]