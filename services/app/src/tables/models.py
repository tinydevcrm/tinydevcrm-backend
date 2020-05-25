"""
Django models for tables service.
"""

import os

from django.conf import settings
from django.db import models

from authentication import models as auth_models


TABLE_URL = 'tables'
TABLE_ROOT = os.path.join(
    settings.MEDIA_ROOT,
    TABLE_URL
)


class DataFile(models.Model):
    """
    Model for data files uploaded to TinyDevCRM.

    Currently, this is used as a file store only, and deleted immediately after
    translated to a PostgreSQL persist-based table after saving.

    TODO: If backups rely on exporting to Parquet, model backups with this
    DataFile model as well.

    TODO: If foreign tables are desired as end-goals, model foreign tables with
    this DataFile model, and develop a strategy to locate files based on user
    ID.
    """
    file_id = models.AutoField(primary_key=True)
    file = models.FileField(
        upload_to=TABLE_URL,
        blank=False,
        null=False
    )

    def __str__(self):
        return str(self.file.name)


class Table(models.Model):
    """
    Model for referencing tables.

    On deletion of the user, restrict the table:
    https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.ForeignKey.on_delete

    TODO: This model may be necessary for referencing PostgreSQL tables with
    owners, and the lifecycle of those tables. However, true existence of tables
    relies on a specific user-ID based PostgreSQL schema. In addition,
    materialized views exist with tables on a one-to-many basis, and cannot
    strictly be modeled as queries are defined as unstructured text.
    """
    table_name = models.CharField(max_length=255)
    user_id = models.ForeignKey(
        auth_models.CustomUser,
        to_field='id',
        on_delete=models.PROTECT
    )
