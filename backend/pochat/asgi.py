import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# from notifications.routing import websocket_urlpatterns as notification_urls

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pochat.settings')

django_asgi_app = get_asgi_application()
from chat.routing import websocket_urlpatterns as chat_urls


application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(
            chat_urls
        ))
    )
})