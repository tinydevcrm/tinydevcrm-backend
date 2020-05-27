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
    ),
    path(
        '<uuid:identifier>/open/',
        views.OpenChannelView().as_view(),
        name='channel_open'
    ),
    path(
        '<uuid:identifier>/close/',
        views.CloseChannelView().as_view(),
        name='channel_close'
    ),
    path(
        '<uuid:identifier>/listen/',
        views.ListenChannelView().as_view(),
        name='channel_listen'
    )
]
