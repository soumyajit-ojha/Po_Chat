from django.urls import re_path
from .consumers import ChatConsumer
from channels.auth import AuthMiddlewareStack

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_name>[-\w]+)/$', AuthMiddlewareStack(ChatConsumer.as_asgi())),
]