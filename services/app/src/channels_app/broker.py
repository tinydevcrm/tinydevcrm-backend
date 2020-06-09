"""
Broker definition. Moved into separate file, as adding directly to a separate
command prevents usage in debugging within `python manage.py shell` or usage
outside of the command process.
"""

import json
import select

import django_eventstream
import psycopg2
from psycopg2 import sql

from core import app_logging
from core import utils as core_utils
from views import models as view_models
from channels_app import models
from channels_app import views


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
    logger = app_logging.get_broker_logger()

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
                logger.info("No information from handler yet.")
            else:
                psql_conn.poll()
                while psql_conn.notifies:
                    # NOTE: Processing one event at a time should be
                    # fine...there should be no need for something like
                    # 'multiprocessing', the load shouldn't be there. Update if
                    # different in production.
                    #
                    # NOTE: Need to pop off psql_conn.notifies to avoid
                    # infinite loop while psql_conn.notifies exists. This
                    # processes multiple notifications correctly.
                    notify = psql_conn.notifies.pop(0)
                    payload = json.loads(notify.payload)
                    job_id = payload['job_id']
                    view_id = payload['view_id']

                    logger.info("Payload: ", payload)

                    view_name = view_models.MaterializedView.objects.filter(id=view_id)[0].view_name

                    logger.info('Materialized view name: ', view_name)

                    channels = models.Channel.objects.filter(
                        job_id=job_id
                    )

                    for channel in channels:
                        logger.info(
                            'Sending update to channel UUID: ',
                            channel.public_identifier
                        )
                        django_eventstream.send_event(
                            str(channel.public_identifier),
                            'message',
                            {
                                'update_available': 'true',
                                'view_name': view_name
                            }
                        )
