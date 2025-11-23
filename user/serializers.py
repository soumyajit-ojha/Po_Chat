"""
This module contains serializer for use model.
"""

from rest_framework import serializers
from .models import User
from .utils import (
    validate_phone_number,
    validate_name,
    validate_email,
    validate_password,
    validate_uploaded_file,
)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User Model
    """

    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        """Meta class for userserializer"""

        model = User
        fields = [
            "id",
            "email",
            "username",
            "phone_number",
            "password",
            "date_joined",
            "last_login",
            "profile_image",
            "hide_email",
        ]

    def validate_email(self, value):
        """validate email"""
        if not value:
            raise serializers.ValidationError("Email Must required.")
        print("Email validation passed")
        return validate_email(value)

    def validate_username(self, value):
        """validate name"""
        if not value:
            raise serializers.ValidationError("Username must required.")
        return validate_name(value)

    def validate_phone_number(self, value):
        """validate phone number"""
        if value:
            return validate_phone_number(value)
        return None

    def validate_password(self, value):
        """validate password"""
        return validate_password(value)

    # def validate_profile_image(self, value):
    #     """validate profile image"""
    #     if value:
    #         allowed_format = (".png", ".jpeg", ".jpg")
    #         max_size = 5
    #         return validate_uploaded_file(value, allowed_format, max_size)
    #     return None
