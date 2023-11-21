# """
# ASGI config for bookingbackend project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
# """

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookingbackend.settings')


# import django


# # routing.py
# from channels.routing import ProtocolTypeRouter, URLRouter
# from chats.routing import  websocket_urlpatterns
# # from channels.auth import AuthMiddlewareStack
# from django.core.asgi import get_asgi_application

# django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     "websocket": 
#         URLRouter(
#             websocket_urlpatterns
#         )
    
# })

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookingbackend.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from channels.routing import ProtocolTypeRouter, URLRouter
from chats.routing import websocket_urlpatterns

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": (
            (URLRouter(websocket_urlpatterns))
        ),
    }
)