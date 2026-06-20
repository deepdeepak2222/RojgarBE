"""Tests for self-serve signup."""
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from clients.models import Client

from .models import Membership

User = get_user_model()


class SignupTests(APITestCase):
    def _signup(self, **overrides):
        payload = {
            "business_name": "Acme Traders",
            "phone": "9876543210",
            "password": "supersecret1",
        }
        payload.update(overrides)
        return self.client.post("/api/auth/signup/", payload, format="json")

    def test_signup_without_email_succeeds(self):
        response = self._signup()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Membership.objects.count(), 1)

    def test_duplicate_phone_is_rejected(self):
        self._signup()
        response = self._signup(business_name="Other")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_phone_is_rejected(self):
        response = self._signup(phone="12")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
