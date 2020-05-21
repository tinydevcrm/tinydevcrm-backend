from django.db import models

# Create your models here.

# TODO: Create association between user and table, if sharding data files by
# user is relevant.

import os

from django.conf import settings
from django.db import models


CONCRETE_TABLE_URL = 'concrete-tables'
CONCRETE_TABLE_ROOT = os.path.join(
    settings.MEDIA_ROOT,
    CONCRETE_TABLE_URL
)


class DataFile(models.Model):
    """
    Model for data files uploaded to TinyDevCRM.
    """
    file_id = models.AutoField(primary_key=True)
    file = models.FileField(
        upload_to=CONCRETE_TABLE_URL,
        blank=False,
        null=False
    )

    def __str__(self):
        return str(self.file.name)
