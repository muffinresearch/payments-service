import json

from django.conf.urls import patterns, url
from django.test import TestCase as DjangoTestCase
from django.test.utils import override_settings

import mock
from rest_framework.views import APIView

from . import dynamic_urls


class APIMock(mock.Mock):
    """
    A mock wrapper that you should use for any curling/slumber API object.
    """

    def tolist(self, *args, **kw):
        """
        DRF can get into a infinite loop with Mock on this method. If you
        override the mock so it returns a value it works.

        This is a hack of the worst kind.
        """
        raise RuntimeError(
            'Attempt to serialise a Mock without the result being overridden.')


class TestCase(DjangoTestCase):

    def json(self, response):
        return response, json.loads(response.content)


# This sets up a module that we can patch dynamically with URLs.
@override_settings(ROOT_URLCONF='payments_service.base.tests.dynamic_urls')
class WithDynamicEndpoints(DjangoTestCase):
    """
    Mixin to allow registration of ad-hoc views.
    """

    def endpoint(self, view):
        """
        Register a view function or view class temporarily
        as the handler for requests to /dynamic-endpoint
        """
        try:
            is_class = issubclass(view, APIView)
        except TypeError:
            is_class = False
        if is_class:
            view = view.as_view()
        dynamic_urls.urlpatterns = patterns(
            '',
            url(r'^dynamic-endpoint$', view),
        )
        self.addCleanup(self._clean_up_dynamic_urls)

    def _clean_up_dynamic_urls(self):
        dynamic_urls.urlpatterns = None


class SolitudeTest(TestCase):

    def setUp(self):
        p = mock.patch('payments_service.solitude.api')
        api = p.start()
        self.addCleanup(p.stop)
        self.solitude = APIMock()
        api.return_value = self.solitude
