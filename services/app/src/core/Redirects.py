"""
Views for redirection.

Having a default Django view, and not erroring out for the root route, may be
necessary in order to keep the Django backend running on AWS ECS.
"""

import textwrap

from django.views.generic.base import View
from django.shortcuts import redirect


class RedirectToDocsView(View):
    """
    Redirects to the API documentation @ https://docs.tinydevcrm.com.
    """
    def dispatch(*args, **kwargs):
        return redirect('https://docs.tinydevcrm.com')
