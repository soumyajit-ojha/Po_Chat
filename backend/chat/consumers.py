import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from .models import Message, ChatRoom
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 1. Authenticate connection
        if self.scope["user"] == AnonymousUser():
            await self.close(code=4001)  # Unauthorized
            return

        # 2. Join room group
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # 3. Notify group about new user
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "system_message",
                "message": f"{self.user.username} joined the chat",
                "username": "System"
            }
        )

    async def disconnect(self, close_code):
        # 1. Leave room group
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

            # 2. Notify group about user leaving
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "system_message",
                    "message": f"{self.user.username} left the chat",
                    "username": "System"
                }
            )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message", "").strip()
            
            if not message:
                raise ValueError("Empty message")

            # Save message to database
            await self.save_message(self.user, self.room_name, message)

            # Broadcast to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": self.user.username,
                    "timestamp": str(self.user.last_login)  # Example additional field
                }
            )

        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                "error": "Invalid JSON format"
            }))
        except ValueError as e:
            await self.send(text_data=json.dumps({
                "error": str(e)
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                "error": "Server error"
            }))
            print(f"Error: {str(e)}")  # Log for debugging

    # Handler for chat messages
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat",
            "message": event["message"],
            "username": event["username"],
            "timestamp": event.get("timestamp", "")
        }))

    # Handler for system messages
    async def system_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "system",
            "message": event["message"],
            "username": event["username"]
        }))

    @sync_to_async
    def save_message(self, user, room_name, message):
        try:
            room = ChatRoom.objects.get(name=room_name)
            Message.objects.create(
                sender=user,
                room=room,
                content=message
            )
        except ObjectDoesNotExist:
            raise ValueError("Chat room does not exist")
        except Exception as e:
            raise Exception(f"Failed to save message: {str(e)}")