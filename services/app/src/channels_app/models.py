"""
Django models for channels service.
"""

import os
import uuid

from django.conf import settings
from django.contrib.postgres import fields as psql_fields
from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication import models as auth_models
from jobs import models as jobs_models


CHANNELS_URL = 'channels'
CHANNELS_ROOT = os.path.join(
    settings.MEDIA_ROOT,
    CHANNELS_URL
)


class EnumChannelStatusTypes(models.TextChoices):
    ACTIVE = 'ACTIVE',_('Channel is open and active, currently sending events out')
    INACTIVE = 'INACTIVE',_('Channel has been created, but is not active')


def default_channels_json_payload():
    """
    Wraps the default JSON payload for the Django channels model in order to
    enforce immutability.
    """
    return {
        'update_available': 'true'
    }


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
    storedprocedure_file = models.FileField(
        null=True,
        upload_to=CHANNELS_URL
    )
    channel_status = models.CharField(
        max_length=16,
        choices=EnumChannelStatusTypes.choices,
        default=EnumChannelStatusTypes.INACTIVE
    )
    json_payload = psql_fields.JSONField(
        default=default_channels_json_payload
    )
