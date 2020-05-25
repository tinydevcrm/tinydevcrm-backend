"""
Table service custom views.
"""

import datetime
import json
import os

from django.conf import settings
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

        file_abspath = os.path.join(
            settings.MEDIA_ROOT,
            datafile.file.name
        )

        temp_table_name = f'temp_{str(request.user.id)}_created_{int(datetime.datetime.now().timestamp())}'

        copy_table_sql_query = sql.SQL(
            'CREATE TABLE {table_name} AS TABLE {temp_table_name} WITH DATA'
        ).format(
            table_name=sql.Identifier(table_name),
            temp_table_name=sql.Identifier(temp_table_name)
        )

        drop_temp_table_sql_query = sql.SQL(
            'DROP FOREIGN TABLE {temp_table_name}'
        ).format(
            temp_table_name=sql.Identifier(temp_table_name)
        )

        # Add error handling logic within this with block if there are numerous
        # HTTP 500 errors that appear in logs.
        with core_utils.PostgreSQLCursor(db_schema=request.user.id) as (psql_conn, psql_cursor):
            # Dynamic column creation makes table creation query much more
            # tricky.
            columns = json.loads(request.data.get('columns'))
            column_names = [
                column_def['column_name']
                for column_def
                in columns
            ]
            column_types = [
                column_def['column_type'].upper()
                for column_def
                in columns
            ]
            column_query = sql.SQL(',').join([
                sql.SQL('{} {}').format(
                    sql.Identifier(column_name),
                    sql.Placeholder()
                )
                for column_name
                in column_names
            ])

            create_foreign_table_sql_query = sql.SQL(
                'CREATE FOREIGN TABLE {temp_table_name} ({columns}) SERVER parquet_srv OPTIONS (filename {file_abspath});'
            ).format(
                temp_table_name=sql.Identifier(temp_table_name),
                columns=column_query,
                file_abspath=sql.Literal(file_abspath)
            )
            create_foreign_table_sql_query = create_foreign_table_sql_query.as_string(psql_conn)

            # TODO: I am concerned this may be a little insecure, since I am not
            # referencing the DB API when templating this string. This has to be
            # done because psycopg2.sql wraps elements within singly or doubly
            # quoted strings, but column types are not strings. I think this
            # should be fine because I can validate recognized column types as
            # enumerations. That hasn't been done yet.
            create_foreign_table_sql_query = create_foreign_table_sql_query % tuple(column_types)

            psql_cursor.execute(create_foreign_table_sql_query)

            psql_cursor.execute(copy_table_sql_query)
            psql_cursor.execute(drop_temp_table_sql_query)
            psql_conn.commit()

            table_serializer = serializers.TableSerializer(
                data={
                    'table_name': table_name,
                    'user': request.user.id
                }
            )
            if table_serializer.is_valid():
                table_serializer.save()

            datafile.delete()
            # Deleting the data model does not delete the file. Do that
            # separately.
            os.remove(os.path.abspath(os.path.join(
                settings.MEDIA_ROOT,
                str(datafile.file)
            )))

        return Response(
            file_serializer.data,
            status=status.HTTP_201_CREATED
        )
