from django.contrib.auth.models import AbstractBaseUser
from django.db import models


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
