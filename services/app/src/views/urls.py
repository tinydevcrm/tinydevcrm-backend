"""
Views service API endpoint configuration.
"""

from django.urls import path

from . import views


urlpatterns = [
    path(
        'create/',
        views.CreateMaterializedViewAPIView().as_view(),
        name='view_create'
    )
]
