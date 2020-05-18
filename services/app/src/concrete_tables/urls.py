"""
Concrete table service API endpoint configuration.
"""

from django.urls import path

from . import views


urlpatterns = [
    path(
        'create/',
        views.CreateTableView().as_view(),
        name='table_create'
    ),
    path(
        'show/',
        views.ShowTableView().as_view(),
        name='table_show'
    )
]
