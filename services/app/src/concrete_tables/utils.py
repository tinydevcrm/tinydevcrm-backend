"""
Utility classes, methods, and variables for concrete table service.
"""

import enum


class RecognizedPostgreSQLTypes(enum.Enum):
    """
    A list of recognized PostgreSQL types, subset of:
    https://www.postgresql.org/docs/12/datatype.html
    """
    # TODO: Implement


def create_table_data_is_valid(request_body):
    """
    Validates whether the request body posted to /tables/create/ is valid.

    Request data is expected in the following format ONLY:

    {
        "name": "some_table",
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

    if sorted(request_body.keys()) != sorted([NAME, COLUMNS]):
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
