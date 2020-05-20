"""
Models for managing file uploads.
"""

import os

from django.conf import settings
from django.db import models


CONCRETE_DATA_URL = 'concrete-data'
CONCRETE_DATA_ROOT = os.path.join(
    settings.MEDIA_ROOT,
    CONCRETE_DATA_URL
)


class File(models.Model):
    """
    Model for files uploaded to TinyDevCRM.
    """
    file_id = models.AutoField(primary_key=True)
    file = models.FileField(
        upload_to=CONCRETE_DATA_URL,
        blank=False,
        null=False
    )

    def __str__(self):
        return str(self.file.name)
