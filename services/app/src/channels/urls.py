"""
Channels service API endpoint configuration.
"""

from django.urls import path

from . import views


urlpatterns = [
    path(
        'create/',
        views.CreateChannelView().as_view(),
        name='channel_create'
    )
]
