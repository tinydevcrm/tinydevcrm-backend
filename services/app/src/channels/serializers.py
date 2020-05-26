"""
Channels service serializers.
See: https://www.django-rest-framework.org/tutorial/1-serialization/
"""

from rest_framework import serializers

from . import models


class ChannelModelSerializer(serializers.ModelSerializer):
    """
    Serializer for the Channel model.
    """
    class Meta:
        model = models.Channel
        fields = "__all__"
