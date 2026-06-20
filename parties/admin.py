from django.contrib import admin

from .models import Party


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ["name", "party_type", "phone", "opening_balance"]
    list_filter = ["party_type"]
    search_fields = ["name", "phone", "email"]
