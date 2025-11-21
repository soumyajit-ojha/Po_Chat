"""
All serializers related to User account
"""
import re

from rest_framework import serializers

from account.models import Account
from core.utils.constants import MAX_IMAGE_SIZE

class AccountSerializer(serializers.ModelSerializer):
    """Serializer for create and update a user account"""
    email = serializers.EmailField(required=True, allow_blank=False)
    username = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        """Meta class"""
        model=Account
        fields=[
            "email",
            "username",
            "profile_image",
            "hide_email"
        ]
    def validate_email(self, attrs):
        """validate email fields in this serializer."""
        email = attrs.strip()
        if not email or not email.strip():
            raise serializers.ValidationError("Email is required.")
        email = email.strip()
        if not re.match(r"^[a-z0-9._%-]+@[a-z0-9.-]+\.[a-z]{2,}$", email):
            raise serializers.ValidationError(
                "Email must be lowercase and in valid format (e.g., dummy12@email.com)."
            )
        return email
    def validate(self, attrs):
        username = attrs.strip()
        if not username or not username.strip():
            raise serializers.ValidationError("Client name is required.")
        username = username.strip()
        if not re.match(r"^[A-Za-z .,'\-]+$", username):
            raise serializers.ValidationError(
                "Client name can only contain letters, spaces, and basic punctuation (.,'-)."
            )
        return username
    def validate_profile_image(self, file):
        """Custom validator for profile_image field."""
        if file and file.size > MAX_IMAGE_SIZE:
            max_mb = MAX_IMAGE_SIZE // (1024 * 1024)
            raise serializers.ValidationError(
                f"File size should not exceed {max_mb} MB."
            )
        return file
