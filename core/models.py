"""Shared base model for anything owned by a single client (tenant).

Inheriting this adds the `client` foreign key with cascade delete, so every
feature gets tenant ownership for free and stays consistent.
"""
from django.db import models

from clients.models import Client


class TenantOwnedModel(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_set",
    )

    class Meta:
        abstract = True
