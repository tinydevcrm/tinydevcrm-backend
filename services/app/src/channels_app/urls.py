"""
Channels service API endpoint configuration.
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
        views.listen,
        name='channel_listen'
    ),
    path(
        # NOTE: Not using uuid:identifier, since protocol handling of identifier
        # is done by dependency. Dependency assumed to expect string and avoid
        # UUID parsing, therefore strip UUID casting.
        '<identifier>/events/',
        include(django_eventstream.urls),
        {
            'format-channels': ['{identifier}']
        }
    )
]
