"""
Custom 'django-admin' command in order to start a background process in order to
translate events published to a channel on the database instance to HTTP/2
Server-Sent Events via reverse proxy.

Since only one master top-level process is needed for a single webapp instance,
and since no complex routing logic is needed (increased load results in a
different design using ZMQ pub/sub between the database and the reverse proxy
without using the webapp as a middleman), a message queue / message broker like
Celery / RabbitMQ / Redis appears as overkill.

The background process relies on Django models existing, because the dependency
relies on the database as a backing store for storing instances of background
task definitions. Therefore, it cannot be scripted into the AppConfig, as the
AppConfig is run during every 'django-admin' management operation, including the
'migrate' command.

One benefit of adding a top-level command is a Docker container can extend the
base image and run separately from the master Django webapp process, and since
the "background" process runs as PID 1 within that container, the task does not
need to be asynchronous, and logs can be directed viewed via 'docker logs'. This
should make for much easier deployment to AWS ECS.
"""

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from channels_app import broker


class Command(BaseCommand):
    help = 'Starts the background process to broker messages between channels on the PostgreSQL database and the Pushpin reverse proxy.'

    def handle(self, *args, **kwargs):
        broker.broker_proc()
