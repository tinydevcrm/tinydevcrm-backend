"""
Startup configuration for Django app 'channels_app'.
"""

import os

from django.apps import AppConfig
from django.db.migrations.executor import MigrationExecutor
from django.db import connections
from django.db import DEFAULT_DB_ALIAS

from core import utils as core_utils


def is_database_synchronized(database):
    """
    This method checks to see whether all database migrations have been run.
    This is important, because starting up the Django application involves
    running a SQL file to define and load triggers and functions, and the SQL
    file will error out if the migrations are not run beforehand, since the
    tables it relies on are undefined.

    See Stack Overflow answer: https://stackoverflow.com/a/31847406

    NOTE: Django only has the one lifecycle hook, 'def ready()', which does not
    provide any granularity into what lifecycles there might exist and is run
    for every Django call, like any command for 'manage.py'. Other methods are
    not meant to be overwritten. Added ticket here:
    https://code.djangoproject.com/ticket/31658

    This file can be located with the PostgreSQL instance. However, since it
    references the underlying Django models, which may change over time and
    changes much more frequently than the database might, adding this file on
    the database side may prove more hassle than it's worth.

    NOTE: This implies that multiple runs of the Django application are required
    in order for the 'ready()' method to be run multiple times. Make sure it is
    done so in order to successfully load the SQL query.

    TODO: Consider having lifecycle-based API endpoints instead of relying on
    the Django lifecycle methods, especially if stored procedures are
    idempotent, and make sure that they're restricted to admin users and logged.

    Args:
        str: Database alias, likely referencable from 'core/settings.py'.
    """
    connection = connections[database]
    connection.prepare_database()
    executor = MigrationExecutor(connection)
    targets = executor.loader.graph.leaf_nodes()
    return not executor.migration_plan(targets)


class ChannelsConfig(AppConfig):
    # Renaming due to conflict from 'django-channels'
    name = 'channels_app'

    def ready(self):
        """
        Method override for startup of channels Django app.

        NOTE: In order for this class to be used at all, reference in
        'INSTALLED_APPS' in 'core/settings.py', as per
        https://stackoverflow.com/a/37430196. This method alone is safe to
        override, as the superclass has an empty method definition.

        NOTE: In order to list all functions in PostgreSQL, open `psql` and run
        `\df+`.

        NOTE: This method MUST be idempotent, since it is run upon every refresh
        of the ASGI server!

        NOTE: Make sure to run container startup after running 'python manage.py
        migrate'!
        """
        # NOTE: This is no way in order to run 'python manage.py migrate' from
        # within this command, since it would recurse and become an infinite
        # loop. Hence, no 'else' command.
        if is_database_synchronized(DEFAULT_DB_ALIAS):
            with core_utils.PostgreSQLCursor() as (psql_conn, psql_cursor):
                stored_procedure_abspath = os.path.abspath(os.path.join(
                    self.name,
                    'storedprocedures',
                    'trigger_on_refresh.sql'
                ))

                stored_procedure_fp = open(stored_procedure_abspath)

                # Execute SQL file: https://stackoverflow.com/a/50080000
                psql_cursor.execute(stored_procedure_fp.read())
                psql_conn.commit()
