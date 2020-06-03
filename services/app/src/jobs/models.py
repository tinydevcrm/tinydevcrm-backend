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

    TODO: While Django migrations will help manage schemas and existing data
    within this table, updating the schema will force an update of the
    unstructured text query during 'SELECT cron.schedule()' in 'jobs/views.py'.
    Usage of unstructured queries is necessary because the Django ORM isn't
    present during cron job execution. Figure out a way in order to generate a
    templatable unstructured query to use in 'jobs/views.py'.

    This limitation should not significantly impact ability to send arbitrary
    JSON payloads over HTTP/2. Since there is a process on the webapp in order
    to broker requests between the database and the reverse proxy, the final
    JSON payload can be constructed by the webapp.

    NOTE: This Django model is highly sensitive! Since the underlying PostgreSQL
    table is referenced by SQL files directly without using the Django ORM,
    including at application startup, running migrations on this table is nigh
    impossible without shutting down the Django application entirely. Field
    definitions should be limited and justified.
    """
    job = models.ForeignKey(
        CronJob,
        on_delete=models.PROTECT,
        to_field='id'
    )
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
