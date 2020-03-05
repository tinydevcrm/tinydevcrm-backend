"""
V1 authentication API models registration.
"""

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Customized user for JWT-based authentication.

    Ideally, this user can be extended in order to provide JWT-based API token
    scoping for various database and backend resources.
    """
