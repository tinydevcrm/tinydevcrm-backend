"""
Django models for views service.
"""

from django.db import models

from authentication import models as auth_models


class MaterializedView(models.Model):
    """
    Django model for materialized view. This model is important for describing
    and managing jobs and channels, as those models have a one-to-one
    relationship with an underlying view.

    TODO: Describe tables with foreign keys and come up with a proper foreign
    key deletion strategy. Right now, since materialized views are described
    with an unstructured query, this isn't possible, though leverage of
    'sql_parse' libraries like 'pglast' and 'psqlparse' may assist things.
    """
    view_name = models.CharField(max_length=255)
    user = models.ForeignKey(
        auth_models.CustomUser,
        on_delete=models.PROTECT,
        to_field='id'
    )
