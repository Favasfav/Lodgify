# routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
import chats.routing
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chats.routing.websocket_urlpatterns
        )
    )
})
