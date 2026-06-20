from django.contrib import admin

from .models import Membership


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ["user", "client", "role", "created_at"]
    list_filter = ["role"]
