"""
Serializers for managing data file uploads.
See: https://www.django-rest-framework.org/tutorial/1-serialization/
See:
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
