"""HTTP layer for Parties. Tenant isolation comes from ClientScopedViewSet."""
from rest_framework import viewsets

from core.scoping import ClientScopedViewSet

from .models import Party
from .serializers import PartySerializer


class PartyViewSet(ClientScopedViewSet, viewsets.ModelViewSet):
    """Full CRUD for parties at /api/parties/, scoped to the user's client."""

    queryset = Party.objects.all()
    serializer_class = PartySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        party_type = self.request.query_params.get("type")
        if party_type:
            queryset = queryset.filter(party_type=party_type)
        return queryset
