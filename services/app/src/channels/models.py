"""
Django models for channels service.
"""

import uuid

from django.db import models

from authentication import models as auth_models
from jobs import models as jobs_models


class Channel(models.Model):
    """
    Model for managing channels.
    """
    # Public identifier of channel, used in URL params.
    public_identifier = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    # TODO: Currently there's a many-to-one correlation between channels and
    # jobs. As in, many channels can reference one job. I think this is
    # backwards, because ideally one channel can listen to many jobs. However,
    # this would imply that a channel has to be created before a job is, or a
    # job has to be updated with a channel after channel creation. Need to go
    # over this data model during a second pass of this project after everything
    # is set up, because a channel should definitely be able to listen to
    # multiple jobs.
    #
    # Just assume a basic one-to-one association for now.
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
