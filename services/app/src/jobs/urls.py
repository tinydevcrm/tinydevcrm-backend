"""
Jobs service API endpoint configuration.
"""

from django.urls import path

from . import views


urlpatterns = [
    path(
        'create/',
        views.CreateJobView().as_view(),
        name='job_create'
    )
]
