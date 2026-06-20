"""A Client is a tenant (a business) using the app.

All business data points back here via a `client` foreign key. Deleting a
client cascades and removes everything that belongs to it.
"""
from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
