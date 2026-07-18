from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "is_active",
        "is_on_trial",
        "trial_ends_at",
        "created_at",
    ]
    list_filter = ["is_active", "is_on_trial"]
    search_fields = ["name"]
    actions = ["disable_clients", "enable_clients"]

    @admin.action(description="Disable selected businesses")
    def disable_clients(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Enable selected businesses")
    def enable_clients(self, request, queryset):
        queryset.update(is_active=True)
