from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatRoom(models.Model):
    """
    Here user1 is the sender and user2 is the receiver.
    with user1 and user2 room is created.
    """
    sender      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatroom_user1')
    receiver    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatroom_user2')

    def __str__(self):
        return f"Chat between {self.sender} and {self.receiver}"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE) # The user1 on room table
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.sender}: {self.content[:20]}"
    
    class Meta:
        ordering = ['-timestamp']