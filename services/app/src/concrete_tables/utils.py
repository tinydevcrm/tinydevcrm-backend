"""
Utility classes, methods, and variables for concrete table service.
"""

import enum
import os

from psycopg2 import sql

from core import utils as core_utils



def create_table_data_is_valid(request_body):
    """
    Validates whether the request body posted to /tables/create/ is valid.

    Request data is expected in the following format ONLY:

    {
        "name": "some_table",
        "dry_run": "0",
        "columns": [
            {
                "name": "some_column",
                "type": "some_type"
            }
        ]
    }

    Args:
        dict: Request body.

    Returns:
        bool: Request body is valid.
    """
    NAME = 'name'
    COLUMNS = 'columns'
    TYPE = 'type'
    DRY_RUN = 'dry_run'

    # TODO: Add check for PostgreSQL schema / table naming conventions.
    # TODO: Add check for PostgreSQL types using Enums.
    # TODO: Create a schema to "walk" along the request body in order to reduce
    # the amount of validation code necessary as the schema expands.

    # NOTE: Use a fine-grained approach to validation in order to preserve as
    # much information about the error as possible for later handling.
    checks = {
        'toplevel_keys_match': True,
        'column_keys_match': True
    }

    if sorted(request_body.keys()) != sorted([NAME, COLUMNS, DRY_RUN]):
        checks['toplevel_keys_match'] = False
        # NOTE: Needs to exit early since validation logic may fail if key
        # 'column' does not exist.
        return all(checks.values())

    for column in request_body.get(COLUMNS):
        if sorted(column.keys()) != sorted([NAME, TYPE]):
            checks['column_keys_match'] = False
            # NOTE: Exiting early by choice, should not error out if no return.
            return all(checks.values())

    return all(checks.values())


def import_data_into_table_request_is_valid(file_path, table_name):
    """
    Validates whether request for API endpoint /v1/tables/import/ is valid.

    Checks for:
    - 'file_path' is a valid path to file.
    - 'table_name' is a valid table.

    Args:
        str: file_path
        str: table_name

    Returns:
        bool: Request is valid.
    """
    # TODO: Add check to ensure schemas between table and file match.

    checks = {
        'file_exists': True,
        'table_exists': True
    }

    # Validate that the file exists.
    if not os.path.exists(file_path):
        checks['file_exists'] = False

    # Validate that the table exists.
    #
    # TODO: Update logic to take into account user-specific schemas if
    # necessary.
    try:
        psql_conn = core_utils.create_fresh_psql_connection()
        psql_cursor = psql_conn.cursor()
        sql_query = sql.SQL(
            'SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name={})'
        ).format(sql.Literal(table_name))
        psql_cursor.execute(sql_query)
        table_exists = psql_cursor.fetchone()[0]
        checks['table_exists'] = table_exists
    except Exception as e:
        checks['table_exists'] = False
    finally:
        psql_cursor.close()
        psql_conn.close()

    return all(checks.values())


def copy_data_into_table(file_path, table_name):
    """
    Copy data from file into table.

    Args:
        str: file_path
        str: table_name
    """
    # TODO: Add method to yield a psql_conn and psql_cursor from within a
    # try/except/finally block in core/utils.py, in order to avoid
    # replicating try/except/finally logic everywhere.
    # TODO: Add support for other kinds of delimiters and choice of CSV
    # headers.
    # TODO: Add better validation, or a way to convert an RFC-4180 compliant
    # CSV into a Parquet file for less risky COPY FROM statements.

    csv_delimiter = ';'

    try:
        psql_conn = core_utils.create_fresh_psql_connection()
        psql_cursor = psql_conn.cursor()

        import ipdb
        ipdb.set_trace()

        # TODO: Add support for CSV headers, right now it's giving me a parsing
        # error for different types and not recognizing the headers for some
        # reason.
        psql_cursor.copy_from(
            open(file_path, 'r'),
            table_name,
            sep=csv_delimiter
        )

        import ipdb
        ipdb.set_trace()

        psql_cursor.execute(sql_query)
        psql_conn.commit()
    except Exception as e:
        # TODO: Have some way of propagating errors gracefully back to the
        # caller
        raise e
    finally:
        psql_cursor.close()
        psql_conn.close()

    pass
