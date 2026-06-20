"""Onboarding: a self-serve signup creates a client (business) and its owner.

The owner's phone number is the login identifier (stored as the username);
email is optional.
"""
from django.contrib.auth import get_user_model
from django.db import transaction

from clients.models import Client

from .models import Membership, Role

User = get_user_model()


@transaction.atomic
def onboard_client(*, business_name: str, phone: str, password: str, email: str = ""):
    client = Client.objects.create(name=business_name)
    owner = User.objects.create_user(
        username=phone, email=email or "", password=password
    )
    Membership.objects.create(user=owner, client=client, role=Role.OWNER)
    return client, owner
