"""
Authentication service custom views.
"""

from django.shortcuts import render
from psycopg2 import sql
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from core import utils as core_utils
from .serializers import CustomTokenObtainPairSerializer, CustomUserSerializer


class CustomObtainTokenPairView(TokenObtainPairView):
    """
    View for generating a custom JWT.
    """
    serializer_class = CustomTokenObtainPairSerializer


class CustomUserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                # If the user is successfully created and saved into the
                # database, create a schema for that user in order to place all
                # subsequent database resources.
                with core_utils.PostgreSQLCursor() as (psql_conn, psql_cursor):
                    create_schema_sql_statement = sql.SQL(
                        "CREATE SCHEMA IF NOT EXISTS {}"
                    ).format(
                        sql.Identifier(str(user.id))
                    )
                    psql_cursor.execute(create_schema_sql_statement)
                    psql_conn.commit()

                json = serializer.data
                return Response(
                    json,
                    status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CustomBlacklistRefreshTokenView(APIView):
    """
    View for blacklisting a refresh JWT.
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )
