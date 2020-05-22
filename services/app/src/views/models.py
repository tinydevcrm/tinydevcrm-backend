"""
Django models for views service.
"""

import enum

from django.db import models
from django.utils.translation import gettext_lazy as _

from . import utils


@utils.register_enum(db_type='views_eventrefreshes_status')
class Status(enum.Enum):
    NEW = 'new'
    SENT = 'sent'

Status.choices = [
    (Status.NEW), _('New event not sent'),
    (Status.SENT), _('Processed event already sent')
]

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

    import ipdb
    ipdb.set_trace()

    materialized_view_name = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.NEW
    )
