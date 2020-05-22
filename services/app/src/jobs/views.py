"""
Jobs service custom API views.
"""

from cron_validator import CronValidator
from psycopg2 import sql
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core import utils as core_utils


class CreateJobView(APIView):
    """
    Handles 'SELECT cron.schedule' requests via API.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request.

        Example:

        curl \
            --header "Content-Type: application/json" \
            --header "Authorization: JWT $JWT_ACCESS_TOKEN" \
            --method POST \
            --data '{"crontab_def", "* * * * *", "view_name": "sample_view"}' \
            https://api.tinydevcrm.com/jobs/create/
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
                'crontab_def_is_valid': True,
                'view_exists': True
            }

            if (
                not request.data.get('crontab_def') or
                not request.data.get('view_name')
            ):
                checks['all_required_keys_are_present'] = False

            # TODO: Implement more comprehensive crontab definition checking.
            # Current validation logic belongs to package 'cron-validator':
            # https://github.com/vcoder4c/cron-validator and coverage /
            # correctness are not as comprehensive as cron definition:
            # https://crontab.guru/
            crontab_def = request.data.get('crontab_def')

            try:
                parsed = CronValidator.parse(crontab_def)
            except Exception as e:
                checks['crontab_def_is_valid'] = False

            view_name = request.data.get('view_name')
            sql_statement = f'SELECT EXISTS(SELECT * FROM pg_matviews WHERE matviewname = \'{view_name}\')'

            try:
                psql_conn = core_utils.create_fresh_psql_connection()
                psql_cursor = psql_conn.cursor()
                psql_cursor.execute(
                    sql.SQL(sql_statement)
                )
                view_exists = psql_cursor.fetchone()[0]
                checks['view_exists'] = view_exists
            except Exception as e:
                return Response(
                    str(e),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            finally:
                psql_cursor.close()
                psql_conn.close()

            return (all(checks.values()), checks)

        (request_is_valid, validation_checks) = _validate(request)

        if not request_is_valid:
            return Response(
                f'Request did not pass validation. Checks: {str(validation_checks)}',
                status=status.HTTP_400_BAD_REQUEST
            )

        crontab_def = request.data.get('crontab_def')
        view_name = request.data.get('view_name')

        sql_statement = f"SELECT cron.schedule('{crontab_def}', 'REFRESH MATERIALIZED VIEW \"{view_name}\"')"

        # TODO: Implement method to fetch from PostgreSQL table 'cron.job' and
        # display cron jobs based on user
        #
        # TODO: Implement method to insert into materialized view refresh events
        # table.

        try:
            psql_conn = core_utils.create_fresh_psql_connection()
            psql_cursor = psql_conn.cursor()
            psql_cursor.execute(
                sql.SQL(sql_statement)
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
            'Successfully created cron job',
            status=status.HTTP_201_CREATED
        )
