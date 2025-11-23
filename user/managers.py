"""
This module ccontains custom user manager for user acconts.
When a new user is created using the create_user method,
It checks for the presence of email and password
"""

from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    This class is used to manage a user and superuser creation.
    """

    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError("email must required.")
        if not password:
            raise ValueError("password must required.")

        user = self.model(
            email=self.normalize_email(email), username=username, **extra_fields
        )
        user.set_password(password)
        user.save(self._db)

    def create_user(self, email, username, password, **extra_fields):
        """Create and save a user with given email and password/"""

        extra_fields.setdefault("is_admin", False)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        """Create and save a super user with given email ans password."""

        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, username, password, **extra_fields)
