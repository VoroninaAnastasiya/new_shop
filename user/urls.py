from django.urls import path

from user import views
from user.views import ProfileUserCreateAPIView, ProfileUserListAPIView, ProfileUserView, ProfileHTMLAPIView

urlpatterns = [
    # path('list_users/', UserAPIView.as_view(), name= 'users'),
    # path('profiles/create/', ProfileUserCreateAPIView.as_view(), name='profile-create'),#можно удалить,тк небезопасен
    path('profile/', ProfileHTMLAPIView.as_view(), name='profile_page'),#можно удалить,тк отдает чужие профили, пока оставляем для проверки метода
    path('api/profile/', ProfileUserView.as_view(), name='profile_api'),

]