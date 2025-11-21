from django.contrib.auth import get_user_model
from friend.models import FriendList
from django.core.exceptions import PermissionDenied

User = get_user_model()

def validate_chat_permission(user, other_user):
    """
    Verify if two users(receiver and sender) are friends and can chat with each other
    Raises PermissionDenied if not friends
    """
    if not (FriendList.objects.filter(user=user, friends=other_user).exists() or
            FriendList.objects.filter(user=other_user, friends=user).exists()):
        raise PermissionDenied("You can only chat with your friends.")

def get_or_create_chatroom(sender, receiver):
    """
    Get or create a chat room between two users after validating friendship
    Returns chatroom if successful, raises PermissionDenied otherwise
    """
    validate_chat_permission(user1, user2)
    
    # Sort users by ID to ensure consistent room creation
    sender, receiver = 
    chat_room, created = ChatRoom.objects.get_or_create(
        sender=sender,
        receiver=receiver
    )
    return chat_room

def get_chatroom_receiver(chat_room, current_user):
    """
    Get the other user in a chat room
    """
    return chat_room.receiver if chat_room.sender == current_user else chat_room.sender