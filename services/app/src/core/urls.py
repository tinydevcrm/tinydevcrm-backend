"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

NOTE: Django REST Framework maintains its own versioning schema to work with
Django's MVC pattern. Use namespace-based versioning to version APIs:
https://www.django-rest-framework.org/api-guide/versioning/#namespaceversioning
"""

import os

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path

from . import Dummy


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    re_path(
        r'^auth/',
        include(
            (
                'authentication.urls',
                'authentication'
            )
        )
    ),
    re_path(
        r'^tables/',
        include(
            (
                'tables.urls',
                'tables'
            )
        )
    ),
    re_path(
        r'^views/',
        include(
            (
                'views.urls',
                'views'
            )
        )
    ),
    re_path(
        r'^jobs/',
        include(
            (
                'jobs.urls',
                'jobs'
            )
        )
    ),
    re_path(
        r'^channels/',
        include(
            (
                'channels.urls',
                'channels'
            )
        )
    ),
    path(
        # Matches the root route only.
        # TODO: Replace with API documentation index.html root.
        '',
        Dummy.HomePageView.as_view(),
        name='rootdummy'
    ),
]
