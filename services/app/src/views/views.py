"""
Views service custom API views.
"""

from psycopg2 import sql
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core import utils as core_utils
from . import utils as views_utils

from . import serializers


class CreateMaterializedViewAPIView(APIView):
    """
    Handles 'CREATE MATERIALIZED VIEW' requests via API.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request.

        TODO: Parse the SQL statement and automatically insert the user ID as
        PostgreSQL schema into the raw SQL statement so that the user doesn't
        need to specify the user ID via the API.

        Example:

        - curl \
            --header "Content-Type: application/json" \
            --header "Authorization: JWT $JWT_ACCESS_TOKEN" \
            --method POST \
            --data '{"view_name": "\"1\".\"sample_view\"", "sql_query": "SELECT * FROM \"1\".\"sample_table\""}' \
            https://api.tinydevcrm.com/views/create/
        """
        def _validate(request):
            """
            Validates request.

            Args:
                rest_framework.request.Request

            Returns:
                (bool, dict): (Request is valid, reasons)
            """
            checks = {
                'all_required_keys_are_present': True,
                'query_starts_with_select_tables_or_values': True,
                'query_does_not_contain_semicolons': True,
                'view_does_not_exist': True
            }

            if (
                not request.data.get('view_name') or
                not request.data.get('sql_query')
            ):
                checks['all_required_keys_are_present'] = False

            sql_query = request.data.get('sql_query')

            # 'sql_query' matches with internal SQL query:
            # https://www.postgresql.org/docs/12/sql-creatematerializedview.html
            if (
                not sql_query.startswith('SELECT') and
                not sql_query.startswith('TABLE') and
                not sql_query.startswith('VALUES')
            ):
                checks['query_starts_with_select_tables_or_values'] = False

            # Prevent some SQL injection attacks by ensuring SQl query does not
            # have semicolon.

            if ';' in sql_query:
                checks['query_does_not_contain_semicolons'] = False

            checks['view_does_not_exist'] = not views_utils.materialized_view_exists(
                str(request.user.id),
                request.data.get('view_name')
            )

            return (all(checks.values()), checks)

        (is_valid_request, validation_checks) = _validate(request)

        if not is_valid_request:
            return Response(
                f'Request did not pass validation. Checks: {str(validation_checks)}',
                status=status.HTTP_400_BAD_REQUEST
            )

        view_name = request.data.get('view_name')
        sql_query_request = request.data.get('sql_query')

        with core_utils.PostgreSQLCursor(db_schema=request.user.id) as (psql_conn, psql_cursor):
            sql_statement = sql.SQL(
                'CREATE MATERIALIZED VIEW {view_name} AS %s WITH DATA'
            ).format(
                view_name=sql.Identifier(view_name)
            )
            sql_statement = sql_statement.as_string(psql_conn)
            sql_statement = sql_statement % sql_query_request

            psql_cursor.execute(
                sql.SQL(sql_statement)
            )
            psql_conn.commit()

            view_serializer = serializers.MaterializedViewSerializer(
                data={
                    'view_name': view_name,
                    'user': request.user.id
                }
            )
            if view_serializer.is_valid():
                view_serializer.save()

        return Response(
            'Successfully created materialized view',
            status=status.HTTP_201_CREATED
        )
