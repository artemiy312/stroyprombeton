"""STB helpers functions and views."""
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from pages.models import Page

from stroyprombeton.models import Product, Category


# Sets CSRF-cookie to CBVs.
set_csrf_cookie = method_decorator(ensure_csrf_cookie, name='dispatch')

MODEL_MAP = {
    'product': Product,
    'category': Category,
    'page': Page
}


def get_keys_from_post(request, *args):
    """Get a list of given keys from request.POST object."""

    return [request.POST.get(arg) for arg in args]
