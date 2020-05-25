"""
Tables service serializers.
See: https://www.django-rest-framework.org/tutorial/1-serialization/
"""

from rest_framework import serializers

from . import models


class DataFileSerializer(serializers.ModelSerializer):
    """
    Serializer for the File model.
    """
    class Meta:
        model = models.DataFile
        fields = "__all__"


class TableSerializer(serializers.ModelSerializer):
    """
    Serializer for the File model.
    """
    class Meta:
        model = models.Table
        fields = "__all__"
