"""
Authentication service models.
"""

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db import models


class CustomManager(BaseUserManager):
    """
    Customized manager for managing CustomUser models and accessing the Django
    admin dashboard; the dashboard breaks otherwise. This is necessary as the
    primary_email for a user is the unique identifier for authentication instead
    of a username. See: https://stackoverflow.com/a/16530435/1497211 and
    https://docs.djangoproject.com/en/dev/topics/auth/customizing/

    This logic is mostly taken from this tutorial:
    https://testdriven.io/blog/django-custom-user-model/#abstractuser-vs-abstractbaseuser
    """
    def create_user(self, email, password, **kwargs):
        """
        Create and save an instance of CustomUser with the given email and
        password.
        """
        if not email:
            raise ValueError(_('Email is required.'))
        email = self.normalize_email(email)
        user = self.model(primary_email=email, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Create and save an instance of CustomUser with superuser privileges.
        """
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if not kwargs.get('is_staff'):
            raise ValueError(_('Superuser must have is_staff=True.'))
        if not kwargs.get('is_superuser'):
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **kwargs)


# Create your models here.
class CustomUser(AbstractBaseUser):
    """
    Customized user for JWT-based authentication.

    Ideally, this user can be extended in order to provide JWT-based API token
    scoping for various database and backend resources.

    NOTE: AbstractBaseUser provides hashed passwords and tokenized password
    resets. Passwords should also be salted by default:
    https://docs.djangoproject.com/en/3.0/topics/auth/passwords/
    """
    objects = CustomManager()

    # Keep the full name around as a Unicode-encoded bytearray:
    # https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/
    #
    # Max length of models.CharField can always be 255:
    # https://stackoverflow.com/a/2597994/1497211
    full_name = models.CharField(max_length=255)

    # Use email as the primary username, since emails address syntax is defined
    # in IEEE RFC-5322: https://tools.ietf.org/html/rfc5322
    primary_email = models.EmailField(unique=True)

    USERNAME_FIELD = 'primary_email'
