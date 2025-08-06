from django.urls import path
from .views import chat_view, send_message  # Split into separate views

urlpatterns = [
    path("chat/<int:chat_room_id>/", chat_view, name="chat_room"),
    path("chat/<int:user_id>/messages/", send_message, name="send_message"),
]