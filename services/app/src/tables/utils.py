"""
Utility classes, methods, and variables for tables service.
"""

from psycopg2 import sql

from core import utils as core_utils


def table_exists(schema_name, table_name):
    """
    Checks whether the table exists.
    """
    with core_utils.PostgreSQLCursor(db_schema=schema_name) as (psql_conn, psql_cursor):
        psql_cursor.execute(
            sql.SQL('SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema = {schemaname} AND table_name = {table_name})').format(
                schemaname=sql.Literal(schema_name),
                table_name=sql.Literal(table_name)
            )
        )
        table_exists = psql_cursor.fetchone()[0]
        return table_exists
