"""
Startup configuration for Django app 'channels_app'.
"""

import os

from django.apps import AppConfig

from core import utils as core_utils


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

        In order to list all functions in PostgreSQL, open `psql` and run
        `\df+`.
        """
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
