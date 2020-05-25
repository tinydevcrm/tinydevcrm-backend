"""
Views service serializers.
See: https://www.django-rest-framework.org/tutorial/1-serialization/
"""

from rest_framework import serializers

from . import models


class MaterializedViewSerializer(serializers.ModelSerializer):
    """
    Serializer for the MaterializedView model.
    """
    class Meta:
        model = models.MaterializedView
        fields = "__all__"
