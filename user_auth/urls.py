from django.urls import path

from .views import RegistrationAPIView, UserListAPIView, LoginAPIView, UserRetrieveUpdateAPIView, LogoutAPIView, \
    LoginHTMLView, LogoutHTMLView, RegistrationHTMLView

app_name = 'user_auth'
urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/register/', RegistrationAPIView.as_view()),
    path('user_list/', UserListAPIView.as_view(), name='user_list'),
    path('users/login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]