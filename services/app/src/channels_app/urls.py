"""
Channels service API endpoint configuration.

NOTE: Not using uuid:identifier, since protocol handling of identifier is done
by dependency. Dependency may be assumed to expect string.
"""

from django.urls import include
from django.urls import path
import django_eventstream

from . import views


urlpatterns = [
    path(
        'create/',
        views.CreateChannelView().as_view(),
        name='channel_create'
    ),
    path(
        '<identifier>/open/',
        views.OpenChannelView().as_view(),
        name='channel_open'
    ),
    path(
        '<identifier>/close/',
        views.CloseChannelView().as_view(),
        name='channel_close'
    ),
    path(
        '<identifier>/listen/',
        include(django_eventstream.urls),
        {
            'format-channels': ['{identifier}']
        }
    )
]
