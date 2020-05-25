"""
Jobs service custom API views.
"""

from cron_validator import CronValidator
from psycopg2 import sql
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core import utils as core_utils
from views import models as view_models
from views import utils as views_utils

from . import serializers


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

            checks['view_exists'] = views_utils.materialized_view_exists(
                str(request.user.id),
                view_name
            )

            return (all(checks.values()), checks)

        (request_is_valid, validation_checks) = _validate(request)

        if not request_is_valid:
            return Response(
                f'Request did not pass validation. Checks: {str(validation_checks)}',
                status=status.HTTP_400_BAD_REQUEST
            )

        crontab_def = request.data.get('crontab_def')
        view_name = request.data.get('view_name')

        view_objects = view_models.MaterializedView.objects.filter(
            user=request.user.id,
            view_name=view_name
        )
        if view_objects.count() != 1:
            return Response(
                'More than one materialized view with the same schema name and view name present. Data corrupted.',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # TODO: Implement method to fetch from PostgreSQL table 'cron.job' and
        # display cron jobs based on user
        # TODO: Implement method to insert into materialized view refresh events
        # table.
        with core_utils.PostgreSQLCursor(db_schema=request.user.id) as (psql_conn, psql_cursor):
            # NOTE: This should be a comprehensive enough filter to get only and
            # only one view.
            sql_statement = sql.SQL(
                "SELECT cron.schedule({}, 'REFRESH MATERIALIZED VIEW {}')"
            ).format(
                sql.Literal(crontab_def),
                sql.Identifier("schema", "table")
            )

            psql_cursor.execute(sql_statement)
            psql_conn.commit()

            job_id = psql_cursor.fetchone()[0]
            view_id = view_objects.first().id

            job_serializer = serializers.CronJobSerializer(
                data={
                    'job_id' : job_id,
                    'user' : request.user.id,
                    'view' : view_id
                }
            )

            if job_serializer.is_valid():
                job_serializer.save()

        return Response(
            'Successfully created cron job',
            status=status.HTTP_201_CREATED
        )
