from django.db.models import Q, Max
from django.shortcuts import render
from friend.models import FriendList
from chat.models import ChatRoom, Message

def home_screen_view(request):
    user = request.user
    if not user.is_authenticated:
        return render(request, 'personal/home.html')


    # Get recent chats with friends (limit 10)
    recent_chat_rooms = (
        ChatRoom.objects.filter(Q(sender=user) | Q(receiver=user))
        .annotate(last_message_time=Max('message__timestamp'))
        .select_related('sender', 'receiver')
        .order_by('-last_message_time')[:10]
    )

    # Prepare chat details
    chat_data = [
        {
            'chat_room': chat,
            'last_message': Message.objects.filter(room=chat).order_by('-timestamp').first()
        }
        for chat in recent_chat_rooms
    ]

    return render(request, 'personal/home.html', {
        'recent_chats': chat_data or None,
    })
