"""Links shared users to the clients (tenants) they belong to, with a role.

Users live in the shared `public` schema; this membership table is how a user
is granted access to a specific client's isolated data.
"""
from django.conf import settings
from django.db import models

from clients.models import Client


class Role(models.TextChoices):
    OWNER = "owner", "Owner"
    STAFF = "staff", "Staff"


class Membership(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="memberships"
    )
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.OWNER
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "client")

    def __str__(self) -> str:
        return f"{self.user} @ {self.client} ({self.role})"
