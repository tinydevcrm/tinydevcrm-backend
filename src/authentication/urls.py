"""
URL configuration for 'authentication'.
"""

from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import ObtainTokenPairWithColorView


urlpatterns = [
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
    )
]
