"""
Event handling service endpoint configuration.
"""

from django.urls import path

from . import views


urlpatterns = [
    path(
        'create/',
        views.CreateEventView().as_view(),
        name='event_create'
    )
]
