"""
Authentication service models.
"""

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Customized manager for managing CustomUser models and accessing the Django
    admin dashboard; the dashboard breaks otherwise. This is necessary as the
    primary_email for a user is the unique identifier for authentication instead
    of a username. See: https://stackoverflow.com/a/16530435/1497211 and
    https://docs.djangoproject.com/en/dev/topics/auth/customizing/

    This logic is mostly taken from this tutorial:
    https://testdriven.io/blog/django-custom-user-model/#abstractuser-vs-abstractbaseuser
    """
    def create_user(self, primary_email, password, full_name, **kwargs):
        """
        Create and save an instance of CustomUser with the given primary_email
        and password.
        """
        if not primary_email:
            raise ValueError('Email is required.')
        primary_email = self.normalize_email(primary_email)
        user = self.model(
            primary_email=primary_email,
            password=password,
            full_name=full_name
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, primary_email, password, full_name, **kwargs):
        """
        Create and save an instance of CustomUser with superuser privileges.
        """
        new_user = self.create_user(
            primary_email,
            password,
            full_name,
            **kwargs
        )

        # NOTE: Might have to issue an additional save with superuser
        # properties. Ideally, these properties can be set in kwargs, and passed
        # to method 'create_user()', which will handle saves at time of user
        # creation.
        new_user.is_staff = True
        new_user.is_active = True
        new_user.is_superuser = True
        new_user.save()

        return new_user


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Customized user for JWT-based authentication.

    Ideally, this user can be extended in order to provide JWT-based API token
    scoping for various database and backend resources.

    NOTE: AbstractBaseUser provides hashed passwords and tokenized password
    resets. Passwords should also be salted by default:
    https://docs.djangoproject.com/en/3.0/topics/auth/passwords/
    """
    objects = CustomUserManager()

    # Keep the full name around as a Unicode-encoded bytearray:
    # https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/
    #
    # Max length of models.CharField can always be 255:
    # https://stackoverflow.com/a/2597994/1497211
    full_name = models.CharField(max_length=255)

    # Use field 'email' as the primary username, since emails address syntax is
    # defined in IEEE RFC-5322: https://tools.ietf.org/html/rfc5322, and because
    # framework likely will not require users to identify each other. If
    # additional emails are registered, use 'secondary_emails' or similar to
    # handle
    primary_email = models.EmailField(unique=True)

    # Default permission levels.
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'primary_email'
    # NOTE: I'm not sure whether it's a good idea to make a full name required.
    # Intended usage at the moment is just as a tag, while the email address
    # should be carried around as the only unique constraint. Having too many
    # unique constraints may make the data model brittle down the line.
    REQUIRED_FIELDS = ['full_name']
