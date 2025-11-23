from django.urls import path

from user.views import ProfileUserCreateAPIView, ProfileUserListAPIView, ProfileUserView

urlpatterns = [
    # path('list_users/', UserAPIView.as_view(), name= 'users'),
    path('profiles/create/', ProfileUserCreateAPIView.as_view(), name='profile-create'),
    path('profiles/', ProfileUserListAPIView.as_view(), name='profiles'),
    path('profile/', ProfileUserView.as_view(), name='user_profile'),
]