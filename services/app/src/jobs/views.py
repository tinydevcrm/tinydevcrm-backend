"""
Jobs service custom API views.
"""

from cron_validator import CronValidator
from django.forms.models import model_to_dict
from psycopg2 import sql
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core import utils as core_utils
from views import models as view_models
from views import utils as views_utils

from . import models
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
        view_id = view_objects.first().id

        with core_utils.PostgreSQLCursor(db_schema=request.user.id) as (psql_conn, psql_cursor):
            # NOTE: The 'INSERT' query references the EventRefreshes Django
            # model, and must be updated manually if the model is updated. See
            # 'jobs/models.py' for more information.
            #
            # TODO: Each channel needs a corrseponding job ID to listen to. That
            # information must be communicated from the event refreshes table,
            # since that is what the underlying trigger listens to. The job ID
            # does not exist until the PostgreSQL function 'cron.schedule' is
            # run. Therefore, the job creation for materialized view, and
            # inserting into the event refreshes table must be split into two
            # components. This may impact the atomicity of operations (e.g. if a
            # refresh event for a materialized view doesn't work, an event may
            # still be sent over the channel), which may impact the amount of
            # work necessary in order to ensure correctness. This might be
            # prevented if job ID was mapped to a list of cron jobs for the
            # CronJob Django model.
            refresh_view_scheduled_query = sql.SQL(
                'REFRESH MATERIALIZED VIEW {view_name}'
            ).format(
                view_name=sql.Identifier(str(request.user.id), view_name)
            )
            refresh_view_sql_statement = sql.SQL(
                "SELECT cron.schedule({crontab_def}, '{scheduled_query}')"
            ).format(
                crontab_def=sql.Literal(crontab_def),
                scheduled_query=refresh_view_scheduled_query
            )
            psql_cursor.execute(refresh_view_sql_statement)
            # NOTE: This commit is necessary in order to get the job ID
            # necessary for insertion into the notify_channel_scheduled_query.
            psql_conn.commit()

            # Create the Django CronJob model.
            job_id = psql_cursor.fetchone()[0]
            job_serializer = serializers.CronJobSerializer(
                data={
                    'job_ids' : [job_id],
                    'user' : request.user.id,
                    'view' : view_id
                }
            )
            if not job_serializer.is_valid():
                return Response(
                    job_serializer.errors(),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            cronjob = job_serializer.save()

            # NOTE: Job ID here refers to the CronJob ID, in order to reference
            # the foreign key for the appropriate channel to send this event on.
            notify_channel_scheduled_query = sql.SQL(
                'INSERT INTO jobs_eventrefreshes(job_id, view_id, created, status) VALUES (\'{job_id}\', \'{view_id}\', NOW(), \'{status}\')'
            ).format(
                job_id=sql.Literal(str(cronjob.id)),
                view_id=sql.Literal(str(cronjob.view.id)),
                status=sql.Literal(str(models.EnumStatusTypes.NEW))
            )
            notify_channel_sql_query = sql.SQL(
                "SELECT cron.schedule({crontab_def}, '{scheduled_query}')"
            ).format(
                crontab_def=sql.Literal(crontab_def),
                scheduled_query=notify_channel_scheduled_query
            )
            psql_cursor.execute(notify_channel_sql_query)
            psql_conn.commit()

            # Update existing cronjob field.
            job2_id = psql_cursor.fetchone()[0]
            cronjob.job_ids = cronjob.job_ids + [job2_id]
            cronjob.save(update_fields=['job_ids'])

        job_data = model_to_dict(cronjob)

        return Response(
            job_data,
            status=status.HTTP_201_CREATED
        )
