"""
Utility classes, methods, and variables for views service.
"""

from psycopg2 import sql

from core import utils as core_utils


def materialized_view_exists(schemaname, matviewname):
    """
    Checks whether materialized view exists.
    """
    with core_utils.PostgreSQLCursor(db_schema=schemaname) as (psql_conn, psql_cursor):
        sql_statement = sql.SQL('SELECT EXISTS(SELECT 1 FROM pg_matviews WHERE schemaname = {schemaname} AND matviewname = {matviewname})').format(
            schemaname=sql.Literal(str(schemaname)),
            matviewname=sql.Literal(matviewname)
        )

        psql_cursor.execute(sql_statement)
        view_exists = psql_cursor.fetchone()[0]

        return view_exists
