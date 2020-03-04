"""
URL configuration for 'authentication'.
"""

from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    ObtainTokenPairWithColorView,
    CustomUserCreate,
    HelloWorldView
)


urlpatterns = [
    path(
        'user/create/',
        CustomUserCreate.as_view(),
        name='create_user'
    ),
    # Override simplejwt stock token
    path(
        'token/obtain/',
        ObtainTokenPairWithColorView.as_view(),
        name='token_create'
    ),
    path(
        'token/refresh/',
        jwt_views.TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'hello/',
        HelloWorldView.as_view(),
        name='hello_world'
    )
]
