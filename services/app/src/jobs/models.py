"""
Django models for jobs service.
"""

from django.db import models

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
