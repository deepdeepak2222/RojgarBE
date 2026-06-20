"""Validation boundary for self-serve signup.

Shop owners sign up with their phone number (the login identifier). Email is
optional.
"""
import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .services import onboard_client

User = get_user_model()

PHONE_PATTERN = re.compile(r"^\+?[0-9]{10,15}$")


class SignupSerializer(serializers.Serializer):
    business_name = serializers.CharField(max_length=120)
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(min_length=8, write_only=True)

    def validate_phone(self, value: str) -> str:
        cleaned = value.replace(" ", "")
        if not PHONE_PATTERN.match(cleaned):
            raise serializers.ValidationError("Enter a valid phone number.")
        if User.objects.filter(username=cleaned).exists():
            raise serializers.ValidationError("This phone is already registered.")
        return cleaned

    def create(self, validated_data):
        client, owner = onboard_client(**validated_data)
        return {"user": owner, "client": client}
