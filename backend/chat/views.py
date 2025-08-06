import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from .models import ChatRoom, Message
from friend.models import FriendList  
from .forms import PrivateChatMessaageForm

User = get_user_model()

@login_required
def chat_view(request, *args, **kwargs):
    user = request.user
    room_id = kwargs.get("room_id")

    if not room_id:
        return JsonResponse({"message":"Chat Room ID missing."})

    chat_room = get_object_or_404(ChatRoom, pk=room_id)

    # Check if the user is part of this chat room
    if user not in [chat_room.sender, chat_room.receiver]:
        return JsonResponse({"message":"You are not authorized to access this chat."})

    # Check if they are friends (optional, depending on your requirements)
    if not FriendList.objects.filter(user=user, friends=chat_room.receiver).exists() and \
       not FriendList.objects.filter(user=user, friends=chat_room.sender).exists():
        return JsonResponse({"message":"You can only chat with your friends."})

    # Determine who is the receiver in this context
    receiver = chat_room.receiver if chat_room.sender == user else chat_room.sender

    # Fetch all messages from this chat room
    chat_messages = Message.objects.filter(room=chat_room).order_by("timestamp")

    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse AJAX request data
            content = data.get("content", "").strip()

            if content:
                message = Message.objects.create(room=chat_room, sender=user, content=content)
                return JsonResponse({
                    "status": "success",
                    "message": message.content,
                    "sender": message.sender.username,
                    "chat_room": chat_room.id,
                })
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid data"}, status=400)

    # Render the chat page for non-AJAX requests
    context = {
        "receiver": receiver,
        "avatar": receiver.profile_image.url if receiver.profile_image else "",
        "messages": chat_messages,
        "form": PrivateChatMessaageForm(), # Ensure form is included
        "chat_room": chat_room, 
    }
    return render(request, "chat/chat_room.html", context)


@login_required
def send_message(request, *args, **kwargs):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            content = data.get("content", "").strip()
            if content:
                room_id = kwargs.get("room_id")
                chat_room = get_object_or_404(ChatRoom, id=room_id)
                
                # Check if user is part of this chat room
                if request.user not in [chat_room.sender, chat_room.receiver]:
                    return JsonResponse({"status": "error", "message": "Unauthorized"}, status=403)
                
                message = Message.objects.create(
                    room=chat_room, 
                    sender=request.user, 
                    content=content
                )
                return JsonResponse({
                    "status": "success", 
                    "message": message.content,
                    "chat_room": chat_room.id,
                })
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid data"}, status=400)
    
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)