from django.contrib import admin
from .models import ChatRoom, Message


class AdminChatRoom(admin.ModelAdmin):
    list_display = ["sender", "receiver"]
    search_fields = ["sender", "receiver"]

    class Meta:
        model = ChatRoom
admin.site.register(ChatRoom, AdminChatRoom)


class AdminChatMessages(admin.ModelAdmin):
    list_display = ["room", "sender", "content"]
    search_fields = ["room", "sender", "content", "timestamp"]
    readonly_fields = ["timestamp"]

    class Meta:
        model = Message
admin.site.register(Message, AdminChatMessages)

