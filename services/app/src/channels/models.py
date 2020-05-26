"""
Django models for channels service.
"""

import uuid

from django.db import models

from authentication import models as auth_models
from jobs import models as jobs_models
from views import models as views_models


class Channel(models.Model):
    """
    Model for managing channels.
    """
    # Public identifier of channel, used in URL params.
    public_identifier = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    job = models.ForeignKey(
        jobs_models.CronJob,
        on_delete=models.PROTECT,
        to_field='job_id'
    )
    user = models.ForeignKey(
        auth_models.CustomUser,
        on_delete=models.PROTECT,
        to_field='id'
    )
    view = models.ForeignKey(
        views_models.MaterializedView,
        on_delete=models.PROTECT,
        to_field='id'
    )
