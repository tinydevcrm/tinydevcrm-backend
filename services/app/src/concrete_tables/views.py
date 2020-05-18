"""
Concrete table service custom views.
"""

from rest_framework.views import APIView


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
            --data '{"table_name": "some_table", "columns": [{"column_name": "columnA", "column_type": "nvarchar(256)"}, {"column_name": "columnB", "column_type": "bytea"}]}'
            https://api.tinydevcrm.com/v1/tables/create/
        """
