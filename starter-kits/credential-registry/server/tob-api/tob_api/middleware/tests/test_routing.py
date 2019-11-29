from unittest.mock import MagicMock, patch

from django.conf import settings
from django.http import HttpRequest
from django.test import TestCase

from ..routing import ApiVersionException, HTTPHeaderRoutingMiddleware


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

        self.assertEqual(result.path_info, self.request.path_info)

    def test_routing_api_call_no_version(self):
        result = self.routing_middleware.process_request(self.request)

        self.assertEqual(result.path_info, self.request.path_info)

    def test_routing_api_call_header_version(self):
        self.request.META["HTTP_ACCEPT"] = "application/json;version=v2"
        result = self.routing_middleware.process_request(self.request)

        self.assertEqual(result.path_info, "/api/v2/some-incredible-method")

    def test_routing_api_call_path_version(self):
        self.request.path_info = "/api/v3/some-incredible-method"
        result = self.routing_middleware.process_request(self.request)

        self.assertEqual(result.path_info, self.request.path_info)

    def test_get_coalesced_request_version_noheader_nopath(self):
        result = self.routing_middleware.get_coalesced_request_version(None, None)

        self.assertEqual(result, settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP["default"])

    def test_get_coalesced_request_version_header_nopath(self):
        result = self.routing_middleware.get_coalesced_request_version("v2", None)

        self.assertEqual(result, "v2")

    def test_get_coalesced_request_version_noheader_path(self):
        result = self.routing_middleware.get_coalesced_request_version(None, "latest")

        self.assertEqual(result, "v3")

    def test_get_coalesced_request_version_header_path_matching(self):
        result = self.routing_middleware.get_coalesced_request_version("latest", "latest")

        self.assertEqual(result, "v3")

    def test_get_coalesced_request_version_header_path_conflicting(self):
        with self.assertRaises(ApiVersionException) as cm:
            result = self.routing_middleware.get_coalesced_request_version("latest", "default")
        
        ex = cm.exception
        self.assertEquals(str(ex), "Conflicting API versions were requested in Accept header [latest] and path [default].")
    
    def test_extract_header_version_noheader(self):
        header_version, request_meta_accept = self.routing_middleware.extract_header_version(self.request)

        self.assertEqual(header_version, None)
        self.assertEqual(request_meta_accept, None)
    
    def test_extract_header_version_header_unsupported(self):
        self.request.META["HTTP_ACCEPT"] = "something-wrong"
        header_version, request_meta_accept = self.routing_middleware.extract_header_version(self.request)

        self.assertEqual(header_version, None)
        self.assertEqual(request_meta_accept, "something-wrong")
    
    def test_extract_header_version_header_noversion(self):
        self.request.META["HTTP_ACCEPT"] = "application/json"
        header_version, request_meta_accept = self.routing_middleware.extract_header_version(self.request)

        self.assertEqual(header_version, None)
        self.assertEqual(request_meta_accept, "application/json")
    
    def test_extract_header_version_header_unsupported(self):
        with self.assertRaises(ApiVersionException) as cm:
            self.request.META["HTTP_ACCEPT"] = "application/json;version=456"
            header_version, request_meta_accept = self.routing_middleware.extract_header_version(self.request)
        
        ex = cm.exception
        self.assertEquals(str(ex), "The specified version [456] is not supported.")
    
    def test_extract_header_version_header_toomany(self):
        with self.assertRaises(ApiVersionException) as cm:
            self.request.META["HTTP_ACCEPT"] = "application/json;version=v2, application/json;version=v3"
            header_version, request_meta_accept = self.routing_middleware.extract_header_version(self.request)
        
        ex = cm.exception
        self.assertEquals(str(ex), "Too many versions were specified in the Accept header.")

    def test_extract_header_version_header_supported(self):
        self.request.META["HTTP_ACCEPT"] = "application/json;version=v2"
        header_version, request_meta_accept = self.routing_middleware.extract_header_version(self.request)

        self.assertEqual(header_version, "v2")
        self.assertEqual(request_meta_accept, "application/json")
