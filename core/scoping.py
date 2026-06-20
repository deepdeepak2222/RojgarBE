"""Enforces tenant isolation in DRF viewsets.

The active client is derived from the logged-in user's membership, so views
never trust a client id sent by the caller. Every read is filtered to that
client and every create is stamped with it.
"""
from rest_framework.exceptions import PermissionDenied


def get_current_client(user):
    membership = user.memberships.select_related("client").first()
    if membership is None:
        raise PermissionDenied("Your account is not linked to any business.")
    return membership.client


class ClientScopedViewSet:
    def get_queryset(self):
        client = get_current_client(self.request.user)
        return super().get_queryset().filter(client=client)

    def perform_create(self, serializer):
        serializer.save(client=get_current_client(self.request.user))
