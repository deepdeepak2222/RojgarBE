"""Tests for the parties feature: auth required + per-client isolation."""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Membership
from clients.models import Client

from .models import Party

User = get_user_model()


class PartyApiTests(APITestCase):
    def setUp(self):
        self.business = Client.objects.create(name="Acme")
        user = User.objects.create_user(username="a@b.com", password="supersecret1")
        Membership.objects.create(user=user, client=self.business)
        self.client.force_authenticate(user=user)

    def test_requires_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/parties/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_stamps_current_client(self):
        response = self.client.post(
            "/api/parties/", {"name": "Cust", "party_type": "customer"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Party.objects.get().client, self.business)

    def test_only_sees_own_clients_parties(self):
        other = Client.objects.create(name="Other")
        Party.objects.create(client=other, name="Foreign", party_type="customer")
        Party.objects.create(client=self.business, name="Mine", party_type="customer")
        response = self.client.get("/api/parties/")
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["name"], "Mine")

    def test_expired_trial_blocks_access(self):
        self.business.trial_ends_at = timezone.now() - timedelta(days=1)
        self.business.save()
        response = self.client.get("/api/parties/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
