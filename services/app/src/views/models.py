"""
Django models for views service.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class EnumStatusTypes(models.TextChoices):
    NEW = 'NEW',_('New event, not processed / sent')
    SENT = 'SENT',_('Processed event already sent')


class EventRefreshes(models.Model):
    """
    Models for issuing materialized view refreshes. This is important because
    trigger definitions for sending out events depend on listening to this table
    specifically for sending out a new event.
    """
    # TODO: Change materialized view name from a plain text file to a reference
    # to a materialized views table for when it becomes user-aware.
    # TODO: Change status from a char field to a custom model field for actual
    # postgresql enum types, potentially adding this to Django middleware:
    # https://schinckel.net/2019/09/18/postgres-enum-types-in-django/
    materialized_view_name = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=16,
        choices=EnumStatusTypes.choices,
        default=EnumStatusTypes.NEW
    )
