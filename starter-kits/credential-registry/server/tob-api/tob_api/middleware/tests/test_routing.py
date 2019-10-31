from unittest.mock import patch, MagicMock

from django.http import HttpRequest
from django.test import TestCase

from ..routing import HTTPHeaderRoutingMiddleware


class Routing_Middleware_TestCase(TestCase):
    routing_middleware: HTTPHeaderRoutingMiddleware = None
    request = None

    def setUp(self):
        get_response_mock = MagicMock()
        self.routing_middleware = HTTPHeaderRoutingMiddleware(get_response_mock)
        self.request = MagicMock(spec=HttpRequest)
        self.request.path_info = "/api/some-incredible-method"
        self.request.META = {}
    
    def tearDown(self):
        self.routing_middleware = None
        self.request = None

    def test_routing_non_api_call(self):
        self.request.path_info = "/not-an-api/a-great-view"
        result = self.routing_middleware.process_request(self.request)
        assert result.path_info == self.request.path_info

    def test_routing_api_call_no_version(self):
        result = self.routing_middleware.process_request(self.request)
        assert result.path_info == self.request.path_info
