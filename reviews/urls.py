from django.urls import path
from .views import ReviewsHTMLView

urlpatterns = [
    path('', ReviewsHTMLView.as_view(), name='reviews_page'),
]
