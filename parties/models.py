"""Data model for a Party: a customer or supplier you trade with."""
from django.db import models

from core.models import TenantOwnedModel


class PartyType(models.TextChoices):
    CUSTOMER = "customer", "Customer"
    SUPPLIER = "supplier", "Supplier"


class Party(TenantOwnedModel):
    name = models.CharField(max_length=120)
    party_type = models.CharField(
        max_length=20,
        choices=PartyType.choices,
        default=PartyType.CUSTOMER,
    )
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    opening_balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "parties"

    def __str__(self) -> str:
        return f"{self.name} ({self.party_type})"
