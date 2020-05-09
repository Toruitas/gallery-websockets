from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
import gallery.routing

application = ProtocolTypeRouter({
    # (http-> Django views is added by default)
    'websocket':
        URLRouter(
            gallery.routing.websocket_urlpatterns,
        )
            
})