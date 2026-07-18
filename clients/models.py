"""A Client is a tenant (a business) using the app.

All business data points back here via a `client` foreign key. Deleting a
client cascades and removes everything that belongs to it.

Access is gated by a trial + an active flag: a new business gets a one-month
free trial, after which it must be kept active (converted) or it loses access.
"""
from datetime import timedelta

from django.db import models
from django.utils import timezone

TRIAL_PERIOD = timedelta(days=30)


def default_trial_end():
    return timezone.now() + TRIAL_PERIOD


class Client(models.Model):
    name = models.CharField(max_length=120)
    is_active = models.BooleanField(
        default=True, help_text="Manual on/off switch for this business."
    )
    is_on_trial = models.BooleanField(
        default=True, help_text="Uncheck once the business has converted (paid)."
    )
    trial_ends_at = models.DateTimeField(default=default_trial_end)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    @property
    def trial_expired(self) -> bool:
        return self.is_on_trial and timezone.now() > self.trial_ends_at

    def has_access(self) -> bool:
        return self.is_active and not self.trial_expired
