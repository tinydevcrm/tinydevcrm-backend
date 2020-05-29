"""
Routing layer for the channels Django app.
"""

from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
from channels.http import AsgiHandler
from django.conf.urls import url
import django_eventstream


urlpatterns = [
    url(
        r'^channels/(?P<identifier>[^/]+)/listen/',
        AuthMiddlewareStack(URLRouter(django_eventstream.routing.urlpatterns)),
        {
            'format-channels': ['{identifier}']
        }
    ),
    url(
        r'',
        AsgiHandler
    )
]
