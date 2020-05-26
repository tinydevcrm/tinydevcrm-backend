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
    def create_user(
            self,
            username,
            primary_email,
            password,
            full_name=None,
            is_staff=False,
            is_superuser=False,
            **kwargs
    ):
        """
        Create and save an instance of CustomUser with the given username,
        primary_email, and password.
        """
        if not primary_email:
            raise ValueError('Email is required.')
        primary_email = self.normalize_email(primary_email)
        user = self.model(
            username=username,
            primary_email=primary_email,
            password=password,
            full_name=full_name
        )
        user.set_password(password)

        # Set permission levels.
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser

        user.save()

        return user

    def create_superuser(self,
        username,
        password,
        primary_email=None,
        full_name=None,
        **kwargs
    ):
        """
        Create and save an instance of CustomUser with superuser privileges.
        """
        # NOTE: Using 'python manage.py createcustomsuperuser' with '--no-input'
        # will successfully parse arguments '--primary-email' and '--password',
        # but using the interactive mode will only recognize 'username' and
        # 'password' only, since it relies on calling super(Command,
        # self).handle().. Primary email cannot be null for users. Therefore, in
        # interactive mode only, hardcode a dummy email to enable superusers to
        # be created interactively given additional command line options.
        if primary_email is None:
            primary_email = 'test@test.com'

        new_user = self.create_user(
            username,
            password,
            primary_email,
            full_name,
            is_staff=True,
            is_superuser=True,
            **kwargs
        )

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
    #
    # Since 'full_name' is just a tag to be carried around and ideally won't be
    # relied on by other portions of the stack, make it nullable in order to
    # make the data model less brittle and more flexible.
    full_name = models.CharField(max_length=255, null=True)

    # Adding a username field in order to
    #
    # NOTE: This username is purely for uniqueness purposes, in order to create
    # multiple apps with the same maintainer email. Underlying database schemas
    # and system dependencies will rely on the auto-incrementing serial primary
    # key ID, and not on the username, as the username is editable.
    username = models.CharField(
        max_length=255,
        null=False,
        unique=True
    )

    # If additional emails are registered, use 'secondary_emails' or similar as
    # a separate field.
    primary_email = models.EmailField(
        null=False,
    )

    # Default permission levels.
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
