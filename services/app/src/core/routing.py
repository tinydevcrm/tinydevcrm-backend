"""
Routing logic for ASGI server.

If there are additional protocols that need to be supported besides HTTP, add
them within this file.
"""

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

from . import urls


application = ProtocolTypeRouter({
    'http': URLRouter(urls.urlpatterns)
})
