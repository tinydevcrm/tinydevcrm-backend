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

import json
import select

from background_task import background
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
import django_eventstream
import psycopg2
from psycopg2 import sql

from views import models as view_models
from channels_app import models
from channels_app import views


@background(queue='channel-broker')
def broker_proc():
    """
    Task definition for broker process to run in compute instance background.
    There should only be one process running, since as the payload is extremely
    light and refreshes are periodic, the load on the process should be
    extremely light and there shouldn't be any reason why the process should
    fall over.

    If liveness issues occur in production, consider installing ZMQ pub/sub on
    the database, and create per-trigger channels, and scale out the database
    and reverse proxy as needed.
    """
    # NOTE: These models aren't imported at the top level because during
    # startup, the models do not yet exist. Otherwise, you will get a
    # 'django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet'.
    # Therefore, only load models during function call.
    # method call.

    CHANNEL_NAME = 'psql_refreshes_channel'

    with core_utils.PostgreSQLCursor() as (psql_conn, psql_cursor):
        psql_conn.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
        )
        sql_statement = sql.SQL("LISTEN {channel}").format(
            channel=sql.Identifier(CHANNEL_NAME)
        )

        psql_cursor.execute(sql_statement)

        while True:
            # If Linux select() syscall returns empty, then do not poll for
            # updates using 'psycopg2'.
            if select.select([psql_conn],[],[],5) == ([],[],[]):
                # NOTE: 'logging.info' does not print to stdout by default
                # here, using print() for convenience.
                print("No information from handler yet.")
            else:
                psql_conn.poll()
                while psql_conn.notifies:
                    # NOTE: This should be fine...there should be no need
                    # for something like 'multiprocessing', the load
                    # shouldn't be there.
                    #
                    # NOTE: Need to pop off psql_conn.notifies to avoid
                    # infinite loop while psql_conn.notifies exists. This
                    # processes multiple notifications correctly.
                    notify = psql_conn.notifies.pop(0)
                    payload = json.loads(notify.payload)
                    job_id = payload['job_id']
                    view_id = payload['view_id']

                    print("Payload: ", payload)

                    view_name = view_models.MaterializedView.objects.filter(id=view_id)[0].view_name

                    print('Materialized view name: ', view_name)

                    channels = models.Channel.objects.filter(
                        job_id=job_id
                    )

                    for channel in channels:
                        print('Sending update to channel UUID: ', channel.public_identifier)
                        django_eventstream.send_event(
                            str(channel.public_identifier),
                            'message',
                            {
                                'update_available': 'true',
                                'view_name': view_name
                            }
                        )


class Command(BaseCommand):
    help = 'Starts the background process to broker messages between channels on the PostgreSQL database and the Pushpin reverse proxy.'


    def handle(self, *args, **kwargs):
        import ipdb
        ipdb.set_trace()

        pass
