"""
Utility classes, methods, and variables relevant to all Django apps within the
backend.
"""

from django.conf import settings
import psycopg2
from psycopg2 import sql


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

DEFAULT_DATABASE_SETTINGS = settings.DATABASES.get('default')
DEFAULT_POSTGRESQL_CONNECTION_CONFIG = {
    'user': DEFAULT_DATABASE_SETTINGS.get('USER'),
    'password': DEFAULT_DATABASE_SETTINGS.get('PASSWORD'),
    'host': DEFAULT_DATABASE_SETTINGS.get('HOST'),
    'port': DEFAULT_DATABASE_SETTINGS.get('PORT'),
    'database': DEFAULT_DATABASE_SETTINGS.get('NAME')
}

class PostgreSQLCursor(object):
    """
    This Python object wraps the 'psycopg2' database connection / cursor object,
    in order to avoid having try/except/finally blocks when interacting with the
    database, and to "float" the context management behavior (e.g. default
    'psycopg2' context management is to close transactions, but not close
    connections and return a connection to the connection pool).

    In addition, since PostgreSQL schemas are created on a user-by-user basis,
    and since explicit schemas make case-sensitivity handling more difficult,
    the database connection / cursor is created on a per-user basis to "lift"
    into the proper schema context.

    Testing against PostgreSQL 12.3 indicates that PostgreSQL functions are
    available within different schemas, as they are available throughout a
    database.
    """

    def __init__(self, db_schema=None, configuration=None):
        """
        Creates a database connection / cursor with user ID and optional
        configuration settings.

        TODO: Validate inputs if necessary.
        """
        self.db_schema = (
            str(db_schema)
            if db_schema
            else 'public'
        )
        self.configuration = (
            configuration
            if configuration
            else DEFAULT_POSTGRESQL_CONNECTION_CONFIG
        )

    def __enter__(self):
        """
        Enter into context management.
        """
        self.conn = psycopg2.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        sql_statement = sql.SQL(
            "SET search_path TO {}"
        ).format(
            sql.Identifier(self.db_schema)
        )
        self.cursor.execute(sql_statement)
        return (self.conn, self.cursor)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit context management.

        TODO: Add commit / rollback code here, if necessary.
        """
        self.cursor.close()
        self.conn.close()
