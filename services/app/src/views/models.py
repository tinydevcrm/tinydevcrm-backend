"""
Django models for views service.
"""

from django.db import models


class EventRefreshes(models.Model):
    """
    Models for issuing materialized view refreshes. This is important because
    trigger definitions for sending out events depend on listening to this table
    specifically for sending out a new event.
    """
    NEW = 'NEW'
    SENT = 'SENT'
    EnumStatusTypes = [
        (NEW, 'Event not processed'),
        (SENT, 'Event already processed / sent')
    ]

    # TODO: Change materialized view name from a plain text file to a reference
    # to a materialized views table for when it becomes user-aware.
    materialized_view_name = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=16,
        choices=EnumStatusTypes,
        default=NEW
    )
