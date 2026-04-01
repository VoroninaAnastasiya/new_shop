from django.urls import path
from .views import ReviewsHTMLView, ReviewSubmitHTMLView, ReviewCreateAPIView

urlpatterns = [
    path('', ReviewsHTMLView.as_view(), name='reviews_page'),
    path('add/', ReviewSubmitHTMLView.as_view(), name='review_add'),
    path('api/reviews/create/', ReviewCreateAPIView.as_view(), name='review_create_api')
]
