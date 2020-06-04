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


class Channel(models.Model):
    """
    Model for managing channels.

    TODO: Somehow integrate active / inactive channel status into the '/listen/'
    API endpoint. Right now, 'listen/' only uses 'django_eventstream' URLs and
    does not tie into the Django ORM models, so each channel does not have
    awareness of whether it is active or not. Therefore, any valid string can be
    a channel to be listened to, instead of only the ones that are declared.

    Originally, I had this snippet of code as part of my Django model:

    class EnumChannelStatusTypes(models.TextChoices):
        ACTIVE = 'ACTIVE',_('Channel is open and active, currently sending events out')
        INACTIVE = 'INACTIVE',_('Channel has been created, but is not active')

    channel_status = models.CharField(
        max_length=16,
        choices=EnumChannelStatusTypes.choices,
        default=EnumChannelStatusTypes.INACTIVE
    )

    TODO: Maybe have the ability to send over JSONified table data, limited to
    some number of records. This was the original intent of having a
    configurable JSON payload. Otherwise, it will always be the same JSON
    payload, which will require another network call by the client in order to
    get the required information.

    Originally, I had this snippet of code as part of the Django model:

    def default_channels_json_payload():
        return {
            'update_available': 'true'
        }

    json_payload = psql_fields.JSONField(
        default=default_channels_json_payload
    )
    """
    # Public identifier of channel, used in URL params.
    public_identifier = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
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
        to_field='id'
    )
    user = models.ForeignKey(
        auth_models.CustomUser,
        on_delete=models.PROTECT,
        to_field='id'
    )
