"""
Utility classes, methods, and variables specific to the channels Django app.
"""

import logging
import os

from django.apps import AppConfig
from django.db.migrations.executor import MigrationExecutor
from django.db import connections
from django.db import DEFAULT_DB_ALIAS

from core import app_logging
from core import utils as core_utils


def is_database_synchronized(database):
    """
    This method checks to see whether all database migrations have been run.
    This is important, because starting up the Django application involves
    running a SQL file to define and load triggers and functions, and the SQL
    file will error out if the migrations are not run beforehand, since the
    tables it relies on are undefined.

    See Stack Overflow answer: https://stackoverflow.com/a/31847406

    Args:
        str: Database alias, likely referencable from 'core/settings.py'.
    """
    connection = connections[database]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    return not executor.migration_plan(targets)


def execute_storedproc_trigger_on_refresh():
    """
    Calls the SQL file 'trigger_on_refresh.sql' in order to execute a PostgreSQL
    trigger upon refresh of the underlying status table.

    NOTE: This method is separate from `apps.py` and `AppConfig().ready()`,
    since resolution for Django ticket #31658
    (https://code.djangoproject.com/ticket/31658) indicates SQL procedures
    should not be run as part of Django lifecycle methods.

    NOTE: To list all functions in PostgreSQL, open `psql` and run `\df+`.

    NOTE: Should use `logging.info`, but `logging` does not print to stdout
    properly in `broker.py`. This issue may have already been addressed, in
    which case switch `print()` statements to `logging.info()` statements.
    """
    logger = app_logging.get_broker_logger()

    if is_database_synchronized(DEFAULT_DB_ALIAS):
        with core_utils.PostgreSQLCursor() as (psql_conn, psql_cursor):
            stored_procedure_abspath = os.path.abspath(os.path.join(
                'channels_app',
                'storedprocedures',
                'trigger_on_refresh.sql'
            ))

            logger.info(
                f'Found stored procedure abspath: {stored_procedure_abspath}'
            )

            stored_procedure_fp = open(stored_procedure_abspath)

            logger.info('Executing SQL file.')

            # Execute SQL file: https://stackoverflow.com/a/50080000
            psql_cursor.execute(stored_procedure_fp.read())
            psql_conn.commit()

            logger.info('Successfully executed SQL file.')
