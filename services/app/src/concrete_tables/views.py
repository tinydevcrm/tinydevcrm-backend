"""
Concrete table service custom views.
"""

import psycopg2
from psycopg2 import sql
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
