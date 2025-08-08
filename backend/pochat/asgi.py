"""
Project ASGI configuration to handle websocket connection.
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from chat.routing import websocket_urlpatterns as chat_urls

# from notifications.routing import websocket_urlpatterns as notification_urls

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pochat.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(
            chat_urls
        ))
    )
})
