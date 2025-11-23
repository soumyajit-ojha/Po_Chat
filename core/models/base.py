"""
This module define base models for application
"""

from django.db import models

class BaseModel(models.Model):
    """
    Base model for all models in this django app.
    Fields includes created_by, created_at, updated_by, updated_at.
    """

    created_by = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="%(class)s_created",
        null=True,
        db_column="Created_By",
        verbose_name="Created By",
    )
    created_dt = models.DateTimeField(auto_now_add=True, db_column="Created_DT")
    updated_by = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated",
        null=True,
        db_column="Updated_By",
        verbose_name="Updated By",
    )
    updated_dt = models.DateTimeField(auto_now=True, db_column="Updated_DT")

    class Meta:
        """Meta class for BaseModel"""
        abstract = True
