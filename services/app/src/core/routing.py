"""
Routing logic for ASGI server.

NOTE: If there are additional protocols that need to be supported besides HTTP,
add them within this file.

NOTE: It looks like the regular urls.py and urlpatterns syntax will work
successfully for 'http' endpoints, and that nesting URLRouter() objects for
multiple different Django applications isn't necessary. Therefore, only create
'routing.py' references and import only the Django applications that require
explicit ASGI/aynchronous support.
"""

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

from channels_app import routing as channels_app_routing


application = ProtocolTypeRouter({
    'http': URLRouter(channels_app_routing.urlpatterns)
})
