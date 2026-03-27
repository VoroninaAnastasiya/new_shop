from django.urls import path

from user import views
from user.views import ProfileUserView, ProfileHTMLAPIView

urlpatterns = [
    path('profile/', ProfileHTMLAPIView.as_view(), name='profile_page'),#можно удалить,тк отдает чужие профили, пока оставляем для проверки метода
    path('api/profile/', ProfileUserView.as_view(), name='profile_api'),

]