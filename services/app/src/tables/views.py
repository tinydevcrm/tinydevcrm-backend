"""
Table service custom views.
"""

import os

import psycopg2
from psycopg2 import sql
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from core import utils as core_utils

from . import utils


class CreateTableView(APIView):
    """
    Handles 'CREATE TABLE' views via API.
    """
    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request.

        Example usage:

        - curl \
            --header "Content-Type: application/json" \
            --header "Authorization: JWT $JWT_ACCESS_TOKEN" \
            --method POST
            --data '{"dry_run": "1", "name": "some_table", "columns": [{"name": "columnA", "type": "nvarchar(256)"}, {"name": "columnB", "type": "bytea"}]}'
            https://api.tinydevcrm.com/v1/tables/create/
        """
        request_body = request.data

        if not utils.create_table_data_is_valid(request_body):
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )

        table_name = request_body.get('name')
        columns = request_body.get('columns')
        column_query = []
        for column in columns:
            column_query.append(
                ' '.join([
                    '"' + column.get('name') + '"',
                    column.get('type').upper()
                ])
            )
        column_query = ', '.join(column_query)
        column_query = '(' + column_query + ')'

        sql_query = f'CREATE TABLE "{table_name}" {column_query};'

        dry_run = int(request_body.get('dry_run'))
        if dry_run:
            return Response(
                {
                    "sql_query": sql_query
                },
                status=status.HTTP_200_OK
            )
        else:
            # NOTE: Wrap connection in try/except/finally block in order to
            # responsibly handle possible errors in executing SQL query.
            try:
                psql_conn = core_utils.create_fresh_psql_connection()
                psql_cursor = psql_conn.cursor()
                psql_cursor.execute(
                    sql.SQL(sql_query)
                )
                psql_conn.commit()
                return Response(
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    str(e),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            finally:
                psql_cursor.close()
                psql_conn.close()


class ShowTableView(APIView):
    """
    Handles 'SHOW TABLE' views via API.
    """
    def get(self, request, *args, **kwargs):
        """
        Handles the HTTP GET request.
        """
        # TODO: Implement.
        pass


class ImportDataIntoTableView(APIView):
    """
    Handles 'COPY INTO' views via API.
    """
    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request.
        """
        file_name = request.data['file']
        table_name = request.data['table']

        # TODO: Change this route by updating the path where the file is
        # retrieved from based on the underlying user, which involves a user
        # model change and migration.
        #
        # TODO: Remove hardcoded nature of 'file'
        file_path = os.path.join(
            models.TABLE_ROOT,
            file_name
        )

        if not utils.import_data_into_table_request_is_valid(
            file_path,
            table_name
        ):
            return Response(
                # TODO: Add better error message on validation details.
                # TODO: Move validation logic from utility method to internal
                # method, since it's only relevant for a specific API endpoint.
                'Invalid request',
                status=status.HTTP_400_BAD_REQUEST
            )

        utils.copy_data_into_table(
            file_path,
            table_name
        )

        return Response(
            'Table is populated with data.',
            status=status.HTTP_200_OK
        )


"""
Concrete data service custom views.
"""

from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers


class FileUploadView(APIView):
    """
    Upload files via API.
    """
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request.

        Example usage:

        - curl \
            --header "Content-Type: multipart/form-data" \
            --header "Authorization: JWT $JWT_ACCESS_TOKEN" \
            --method POST \
            -F file=@sample.csv \
            https://api.tinydevcrm.com/v1/data/upload/

        NOTE: These keys, such as 'data' and 'file', are very particular to the
        underlying models and serializers. Do not change without testing in
        development.
        """

        file_serializer = serializers.FileSerializer(
            # Use the form key 'file=' in order to send binary files as part of
            # a multipart/form-data request.
            #
            # Example: curl --header "Content-Type: multipart/form-data"
            # --header "Authorization: JWT $JWT_ACCESS_TOKEN" -X POST  -F
            # 'file=@"/path/to/sample.csv"'
            # http://localhost:8000/v1/data/upload/
            data={
                'file': request.data['file']
            }
        )
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(
                file_serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                file_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
