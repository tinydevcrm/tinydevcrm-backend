"""
Utility classes, methods, and variables relevant to all Django apps within the
backend.
"""

from django.conf import settings
import psycopg2


def create_fresh_psql_connection():
    """
    Creates a fresh PostgreSQL connection (not cached / memoized).

    NOTE: It is the caller's responsibility to shut down the connection in a
    responsible manner.

    Returns:
        psycopg2.extensions.connection: Connection to the current PostgreSQL
        instance.
    """
    default_database_settings = settings.DATABASES.get('default')
    _conn = psycopg2.connect(
        user=default_database_settings.get('USER'),
        password=default_database_settings.get('PASSWORD'),
        host=default_database_settings.get('HOST'),
        port=default_database_settings.get('PORT'),
        database=default_database_settings.get('NAME')
    )
    return _conn
