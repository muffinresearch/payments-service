from django.shortcuts import render
from django.conf import settings


def index(request):
    """Page that serves the HTML for the payments-ui"""
    return render(request, 'base.html', {'static_path': settings.UI_STATIC})


def payment_form(request):
    """Page that serves the HTML for the payments-ui"""
    return render(request, 'payment-form.html',
                  {'static_path': settings.UI_STATIC})
