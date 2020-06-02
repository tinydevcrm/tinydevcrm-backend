"""
Django models for jobs service.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication import models as auth_models
from views import models as view_models


class CronJob(models.Model):
    """
    Model for managing cron jobs.

    TODO: Currently, cron jobs are hardcoded to refresh one materialized view
    only. If there's an extension that breaks the one-to-one association between
    views and jobs, consider a migration.

    TODO: Figure out whether there's a way in order to extend automatically
    created table 'cron.job' for application-specific purposes.
    """
    # ID from table 'cron.job', must be unique because it's referenced as a
    # foreign key by the channels model.
    job_id = models.IntegerField(unique=True)
    user = models.ForeignKey(
        auth_models.CustomUser,
        on_delete=models.PROTECT,
        to_field='id'
    )
    view = models.ForeignKey(
        view_models.MaterializedView,
        on_delete=models.PROTECT,
        to_field='id'
    )


# NOTE: Python-based enum.Enum type underneath the hood, that may map to enum
# types using the Django ORM:
# https://schinckel.net/2019/09/18/postgres-enum-types-in-django/
class EnumStatusTypes(models.TextChoices):
    NEW = 'NEW',_('New event, not processed / sent')
    SENT = 'SENT',_('Processed event already sent')


class EventRefreshes(models.Model):
    """
    Models for issuing materialized view refreshes. This is important because
    trigger definitions for sending out events on a channel depend on listening
    to this table specifically for sending out a new event.

    NOTE: Foreign key references for same-file models must be ordered. See this
    Stack Overflow answer: https://stackoverflow.com/a/17658689
    """
    view = models.ForeignKey(
        view_models.MaterializedView,
        on_delete=models.PROTECT,
        to_field='id'
    )
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=16,
        choices=EnumStatusTypes.choices,
        default=EnumStatusTypes.NEW
    )
