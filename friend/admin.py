from django.contrib import admin
from .models import FriendList, FriendRequest

class FriendListAdmin(admin.ModelAdmin):
    list_display        = ["user"]
    list_filter         = ["user"]
    search_fields       = ["user"]
    readonly_fields     = ["user"]

    class meta:
        model = FriendList
admin.site.register(FriendList, FriendListAdmin)


class FriendRequestAdmin(admin.ModelAdmin):
    list_display        = ["sender", "receiver", "is_active"]
    list_filter         = ["sender", "receiver"]
    readonly_fields     = ["sender", "receiver"]
    search_fields       = ["sender__emai", "sender__username", "receiver__email", "receiver__username"]

    class meta:
        model = FriendRequest
admin.site.register(FriendRequest, FriendRequestAdmin)
