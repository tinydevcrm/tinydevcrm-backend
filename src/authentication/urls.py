"""
URL configuration for 'authentication'.
"""

from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    CustomUserRegister,
    CustomObtainTokenPairView,
    CustomBlacklistRefreshTokenView,
    # HelloWorldView,
)


urlpatterns = [
    path(
        'users/register/',
        CustomUserRegister.as_view(),
        name='users.register'
    ),
    # Override simplejwt stock token
    path(
        'tokens/obtain/',
        CustomObtainTokenPairView.as_view(),
        name='tokens.obtain'
    ),
    path(
        'tokens/refresh/',
        jwt_views.TokenRefreshView.as_view(),
        name='tokens.refresh'
    ),
    path(
        'tokens/blacklist/',
        CustomBlacklistRefreshTokenView.as_view(),
        name='tokens.blacklist'
    )

    # path(
    #     'hello/',
    #     HelloWorldView.as_view(),
    #     name='hello_world'
    # ),
]
