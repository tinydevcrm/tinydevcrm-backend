from django.shortcuts import render
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import MyTokenObtainPairSerializer


# Create your views here.
class ObtainTokenPairWithColorView(TokenObtainPairView):
    # NOTE: Last comma is important, otherwise an iteration error will result
    # because wrapping a str with parens results in str while wrapping str +
    # comma with parens results in tuple
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
