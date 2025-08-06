from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("profile/", views.user_profile_view, name="profile"),
    path("organizer-profile/", views.organizer_profile_view, name="organizer_profile"),
    path("me/", views.current_user_detail, name="current_user"),
]
