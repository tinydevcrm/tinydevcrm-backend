"""
Routing layer for the channels Django app.
"""

from channels.routing import URLRouter
from channels.http import AsgiHandler
from django.conf.urls import url
import django_eventstream

from authentication import authentication


urlpatterns = [
    url(
        r'^channels/?P<identifier>[^/]+/events/',
        authentication.ChannelsTokenAuthMiddleware((
            URLRouter(django_eventstream.routing.urlpatterns)
        )),
        {
            'format-channels': ['{identifier}']
        }
    ),
    url(
        r'',
        AsgiHandler
    )
]
