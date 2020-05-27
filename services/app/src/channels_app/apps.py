from django.apps import AppConfig


class ChannelsConfig(AppConfig):
    # Renaming due to conflict from 'django-channels'
    name = 'channels_app'
