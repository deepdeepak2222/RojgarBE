"""Tests for client trial + active access rules."""
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .models import Client


class ClientAccessTests(TestCase):
    def test_new_client_is_on_trial_with_access(self):
        client = Client.objects.create(name="Fresh")
        self.assertTrue(client.is_on_trial)
        self.assertTrue(client.has_access())

    def test_expired_trial_loses_access(self):
        client = Client.objects.create(
            name="Lapsed", trial_ends_at=timezone.now() - timedelta(days=1)
        )
        self.assertTrue(client.trial_expired)
        self.assertFalse(client.has_access())

    def test_disabled_client_loses_access(self):
        client = Client.objects.create(name="Off", is_active=False)
        self.assertFalse(client.has_access())

    def test_converted_client_keeps_access_after_trial_window(self):
        client = Client.objects.create(
            name="Paid",
            is_on_trial=False,
            trial_ends_at=timezone.now() - timedelta(days=1),
        )
        self.assertTrue(client.has_access())
