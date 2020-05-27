"""
Channels service custom API views.
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
            --data '{"job_id": "some_job_id", "view_name": "some_view_name"}' \
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


class OpenChannelView(APIView):
    """
    Calls trigger to execute 'LISTEN/NOTIFY' events from the database and
    "lifts" them to HTTP context.

    This is managed separately from channel creation because channel management
    lifecycles should be different from channel usage lifecycles, as the former
    should be
    """
    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request.
        """
        import ipdb
        ipdb.set_trace()

        # TODO: Implement
        pass


class CloseChannelView(APIView):
    """
    Calls stored procedure to drop the function and trigger created by channel
    opening.
    """
    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request.
        """
        import ipdb
        ipdb.set_trace()

        # TODO: Implement
        pass


class ListenChannelView(APIView):
    """
    Returns an event stream that continuously sends over data until it is shut
    down.
    """
    def get(self, request, *args, **kwargs):
        """
        Handles the HTTP GET request.
        """
        import ipdb
        ipdb.set_trace()

        # TODO: Implement
        pass
