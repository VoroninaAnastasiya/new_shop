from django.urls import path

from user.views import ProfileUserCreateAPIView, ProfileUserListAPIView, ProfileUserView

urlpatterns = [
    # path('list_users/', UserAPIView.as_view(), name= 'users'),
    path('profiles/create/', ProfileUserCreateAPIView.as_view(), name='profile-create'),#можно удалить,тк небезопасен
    path('profiles/', ProfileUserListAPIView.as_view(), name='profiles'),#можно удалить,тк отдает чужие профили, пока оставляем для проверки метода
    path('profile/', ProfileUserView.as_view(), name='user_profile'),
]