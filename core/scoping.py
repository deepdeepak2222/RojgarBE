"""Enforces tenant isolation + access control in DRF viewsets.

The active client is derived from the logged-in user's membership, so views
never trust a client id sent by the caller. Every read is filtered to that
client and every create is stamped with it. Data access also requires the
client to be active and within its trial.
"""
from rest_framework.exceptions import PermissionDenied


def get_membership_client(user):
    """The user's business, without access checks (for status endpoints)."""
    membership = user.memberships.select_related("client").first()
    if membership is None:
        raise PermissionDenied("Your account is not linked to any business.")
    return membership.client


def get_current_client(user):
    """The user's business, only if it is allowed to use the app right now."""
    client = get_membership_client(user)
    if not client.is_active:
        raise PermissionDenied("This business has been disabled.")
    if client.trial_expired:
        raise PermissionDenied("Your free trial has ended. Please subscribe to continue.")
    return client


class ClientScopedViewSet:
    def get_queryset(self):
        client = get_current_client(self.request.user)
        return super().get_queryset().filter(client=client)

    def perform_create(self, serializer):
        serializer.save(client=get_current_client(self.request.user))
