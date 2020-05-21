"""
Django models for tables service.
"""

import os

from django.conf import settings
from django.db import models


TABLE_URL = 'tables'
TABLE_ROOT = os.path.join(
    settings.MEDIA_ROOT,
    TABLE_URL
)


class DataFile(models.Model):
    """
    Model for data files uploaded to TinyDevCRM.
    """
    file_id = models.AutoField(primary_key=True)
    file = models.FileField(
        upload_to=TABLE_URL,
        blank=False,
        null=False
    )

    def __str__(self):
        return str(self.file.name)
