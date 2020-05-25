"""
Jobs service serializers.
See: https://www.django-rest-framework.org/tutorial/1-serialization/
"""

from rest_framework import serializers

from . import models


class CronJobSerializer(serializers.ModelSerializer):
    """
    Serializer for the CronJob model.
    """
    class Meta:
        model = models.CronJob
        fields = "__all__"
