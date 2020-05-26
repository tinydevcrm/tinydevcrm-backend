"""
Utility classes, methods, and variables for jobs service.
"""

from psycopg2 import sql

from core import utils as core_utils


def cron_job_exists(schemaname, job_id):
    """
    Checks whether cron job exists.

    TODO: Reconcile the jobs Django model with the pg_cron table, because
    they're two separate trackers for the same thing. For now, referencing
    cron.job because it's the source of truth.
    """
    with core_utils.PostgreSQLCursor(db_schema=schemaname) as (psql_conn, psql_cursor):
        sql_statement = sql.SQL(
            "SELECT EXISTS(SELECT 1 FROM cron.job WHERE jobid = {job_id} AND active = 't')"
        ).format(
            job_id=sql.Literal(str(job_id))
        )

        psql_cursor.execute(sql_statement)
        job_exists = psql_cursor.fetchone()[0]

        return job_exists
