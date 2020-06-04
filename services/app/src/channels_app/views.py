"""
Channels service custom API views.

TODO: Channels are unique because 'django_eventstream' and the reverse proxy
(Pushpin) handle the channel opening and closing, not the Django application.
The only thing the application guarantees at the moment is creating and deleting
channels, so that calling <channel-id>/listen/ will actually see results from
the backend. Ideally, channel listening should be validated with the Django
Channels model, and an HTTP 400 Bad Request response should be returned if the
channel UUID does not match.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from jobs import utils as jobs_utils
from . import serializers


class CreateChannelView(APIView):
    """
    Handles channel creation in Django models.
    """
    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request.

        Example:

        curl \
            --header "Content-Type: application/json" \
            --header "Authorization: JWT $JWT_ACCESS_TOKEN" \
            --method POST \
            --data '{"job_id": "some_job_id"}' \
            https://api.tinydevcrm.com/channels/create/
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
                'job_exists': True
            }

            if (
                not request.data.get('job_id')
            ):
                checks['all_required_keys_are_present'] = False

            job_id = request.data.get('job_id')
            checks['job_exists'] = jobs_utils.cron_job_exists(
                str(request.user.id),
                str(job_id)
            )

            return (all(checks.values()), checks)

        (is_valid_request, validation_checks) = _validate(request)

        if not is_valid_request:
            return Response(
                f'Request did not pass validation. Checks: {str(validation_checks)}',
                status=status.HTTP_400_BAD_REQUEST
            )

        job_id = request.data.get('job_id')
        user_id = request.user.id

        channel_serializer = serializers.ChannelModelSerializer(
            data={
                'job' : job_id,
                'user' : request.user.id
            }
        )

        if channel_serializer.is_valid():
            channel_serializer.save()
        else:
            return Response(
                channel_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            channel_serializer.data,
            status=status.HTTP_201_CREATED
        )
