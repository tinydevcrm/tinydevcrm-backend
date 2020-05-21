"""
Concrete table service API endpoint configuration.
"""

# TODO: Implement /show for showing a table.
# TODO: Implement /fork for forking a table to make it mutable.

from django.urls import path

from . import views


urlpatterns = [
    path(
        'create/',
        views.CreateTableView().as_view(),
        name='table_create'
    )
]
