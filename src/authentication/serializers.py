"""
Custom serializers for authentication service.
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from . import models


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        """
        Gets a token, and adds custom attributes / claims, before returning to
        the public view.
        """
        token = super(
            CustomTokenObtainPairSerializer,
            cls
        ).get_token(user)

        return token


class CustomUserSerializer(serializers.ModelSerializer):
    """
    (I'm guessing) serializes a model for direct writes to the database.

    TODO: Write a better docstring
    """
    class Meta:
        """
        TODO: Replace docstring, once I know how this class works and why it is
        necessary (copied from tutorial)
        """
        model = models.CustomUser
        fields = ('full_name', 'primary_email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        # TODO: Not sure whether create() can be renamed to register(), who
        # calls this method?
        password = validated_data.pop('password', None)
        # As long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance
