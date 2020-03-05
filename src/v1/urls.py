"""
V1 API endpoint registration.

This file should contain registration of API endpoints from various services,
such as authentication. It should not require or maintain its own models.
"""

from django.urls import include
from django.urls import path


urlpatters = [
    path(
        'auth/',
        include('v1.auth.urls')
    )
]
