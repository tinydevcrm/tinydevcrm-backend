"""
Table service custom views.
"""

import json
import os

from psycopg2 import sql
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers
from core import utils as core_utils


class CreateTableView(APIView):
    """
    Handles 'CREATE FOREIGN TABLE' views via API.
    """
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request.

        These tables are generated from data dumps backed by "concrete data",
        Parquet files available via PostgreSQL extension 'parquet_fdw' (foreign
        data wrapper) that serve as the foundational sources of truth for users.
        This is opposed to "derived data", which is data computed via
        mathematical, logical / relational, or other types of transformations.
        For example, a materialized view would be considered "derived data",
        while a CSV upload would be considered "concrete data".

        Making this distinction guarantees unitary application data flow by
        making sure each layer is immutable (writes are prohibited for foreign
        tables and only occur during HTTP POST), and that consequently,
        underlying data pipelines are acyclic and easier to manage. Since there
        is only one version of the data, versioning and backup of foreign tables
        is fairly trivial.

        TODO: A prior version of this method used to create the foreign table
        as-is. While this would work for creating materialized views and
        triggers, the inability of writes to the underlying data, as well as the
        difficulties managing the persist layer precludes this method as too
        inflexible for OLTP workloads. If foreign tables are desired, create a
        separate endpoint for supporting only foreign tables.

        TODO: Take the complete possible PostgreSQL 'CREATE TABLE' syntax and
        translate that through a form to get the full functionality of 'CREATE
        TABLE' commands without suffering extraneous security issues of doing
        so.

        TODO: In addition, each PostgreSQL table is nested under a user schema
        defined by the custom user, in order to deconflict data resources
        underneath the hood, and to help facilitate schema-based multitenancy.
        Create a PostgreSQL user during the 'CREATE SCHEMA IF NOT EXISTS' in
        order to apply an authorization for the schema to that user, so that
        `psql -h db.tinydevcrm.com -U $CUSTOM_USERNAME` can work properly.

        Example usage:

        - curl \
            --header "Content-Type: multipart/form-data" \
            --header "Authorization: JWT $JWT_ACCESS_TOKEN" \
            --method POST \
            -F file=@sample.parquet \
            -F table_name=sample_table \
            -F columns='[{"column_name": "SomeNumber", "column_type":"int"},{"column_name":"SomeString","column_type":"varchar(256)"}]' \
            https://api.tinydevcrm.com/tables/create/

        NOTE: These keys, such as 'data' and 'file', are very particular to the
        underlying models and serializers. Do not change without testing in
        development.
        """
        def _validate(request):
            """
            Validates request data.

            Args:
                rest_framework.request.Request

            Returns:
                bool: Request is valid.
            """
            checks = {
                'all_required_keys_are_present': True,
                'column_schema_is_valid': True
            }

            if (
                not request.data.get('file') or
                not request.data.get('table_name') or
                not request.data.get('columns')
            ):
                checks['all_required_keys_are_present'] = False

            columns = request.data.get('columns')
            try:
                column_data = json.loads(columns)
                assert type(column_data) is list
                for item in column_data:
                    assert type(item) is dict
                    assert sorted(item.keys()) == ['column_name', 'column_type']
                    # TODO: Add check for column types and column names
            except (Exception, AssertionError) as e:
                checks['column_schema_is_valid'] = False

            return (
                all(checks.values()),
                checks
            )

        (is_valid, validation_checks) = _validate(request)
        if not is_valid:
            return Response(
                f'Request is not valid: {str(validation_checks)}',
                status=status.HTTP_400_BAD_REQUEST
            )

        file_serializer = serializers.DataFileSerializer(
            # Use the form key 'file=@$FILENAME' in order to send binary files
            # as part of a multipart/form-data request.
            data={
                'file': request.data['file']
            }
        )

        if not file_serializer.is_valid():
            return Response(
                file_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        datafile = file_serializer.save()

        table_name = request.data.get('table_name')
        columns = json.loads(request.data.get('columns'))
        column_query = []
        for column in columns:
            column_query.append(
                ' '.join([
                    '"' + column.get('column_name') + '"',
                    column.get('column_type').upper()
                ])
            )
        column_query = ', '.join(column_query)
        column_query = '(' + column_query + ')'

        file_abspath = os.path.join(
            models.TABLE_ROOT,
            request.data.get('file').name
        )
        sql_query = f'CREATE FOREIGN TABLE "{table_name}" {column_query} SERVER parquet_srv OPTIONS (filename \'{file_abspath}\');'

        # NOTE: Wrap connection in try/except/finally block in order to
        # responsibly handle possible errors in executing SQL query.
        try:
            psql_conn = core_utils.create_fresh_psql_connection()
            psql_cursor = psql_conn.cursor()
            psql_cursor.execute(
                sql.SQL(sql_query)
            )
            psql_conn.commit()
        except Exception as e:
            return Response(
                str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            psql_cursor.close()
            psql_conn.close()

        return Response(
            file_serializer.data,
            status=status.HTTP_201_CREATED
        )
