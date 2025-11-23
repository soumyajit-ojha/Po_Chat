"""
This module contains the data model for user accounts.
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager


class User(AbstractBaseUser):
    """
    User Model to store user account information.
    Inherited from BaseModel.
    """

    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(verbose_name="user name", max_length=40)
    phone_number = models.CharField(
        verbose_name="phone_number", max_length=15, blank=True, null=True
    )
    is_verified_email = models.BooleanField(
        default=False,
    )
    is_verified_phone_number = models.BooleanField(
        default=False,
    )
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(
        max_length=200,
        upload_to="user/profile_imges/",
        blank=True,
        null=True,
    )
    hide_email = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return str(self.username)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_lebel):
        return True
