"""
Channels service custom API views.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateChannelView(APIView):
    """
    Handles 'LISTEN/NOTIFY' events from the database and "lifts" them to HTTP
    context.
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
        # TODO: Implement.
        # TODO: Return serializer data instead of text message.
        return Response(
            "Successfully created channel",
            status=status.HTTP_201_CREATED
        )
