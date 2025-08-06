from django.contrib import admin
from . models import Account

class AdminAccount(admin.ModelAdmin):
    list_display = ["id","username", "email", "date_joined", "last_login", "is_admin", "is_staff"]
    search_fields = ["email", "username"]
    readonly_fields = ["date_joined", "last_login"]

admin.site.register(Account, AdminAccount)