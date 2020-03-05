"""
V1 authentication API model registration with Django admin.
"""

from django.contrib import admin

from . import models


class CustomUserAdmin(admin.ModelAdmin):
    model = models.CustomUser


admin.site.register(
    models.CustomUser,
    CustomUserAdmin
)
