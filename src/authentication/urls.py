"""
URL configuration for 'authentication'.
"""

from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    # ObtainTokenPairWithColorView,
    CustomUserRegister,
    # HelloWorldView,
    # LogoutAndBlacklistRefreshTokenForUserView
)


urlpatterns = [
    path(
        'users/register/',
        CustomUserRegister.as_view(),
        name='users.register'
    ),
    # # Override simplejwt stock token
    # path(
    #     'token/obtain/',
    #     ObtainTokenPairWithColorView.as_view(),
    #     name='token_create'
    # ),
    # path(
    #     'token/refresh/',
    #     jwt_views.TokenRefreshView.as_view(),
    #     name='token_refresh'
    # ),
    # path(
    #     'hello/',
    #     HelloWorldView.as_view(),
    #     name='hello_world'
    # ),
    # path(
    #     'blacklist/',
    #     LogoutAndBlacklistRefreshTokenForUserView.as_view(),
    #     name='blacklist'
    # )
]
