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
    # TODO: There are likely constraints within 'cron.job' that can be applied
    # to job ID, not sure whether they can be referenced here since 'cron.job'
    # isn't modeled within Django.
    job_id = models.IntegerField()
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
