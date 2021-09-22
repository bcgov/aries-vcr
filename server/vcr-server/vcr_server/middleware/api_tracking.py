import logging
from time import perf_counter

from django.conf import settings
from django.urls import resolve

from snowplow_tracker import SelfDescribingJson

from .routing import ApiVersionException, HTTPHeaderRoutingMiddleware

LOGGER = logging.getLogger(__name__)


class SnowplowTrackingMiddleware(HTTPHeaderRoutingMiddleware):
    """
    Middleware to emit snowplow tracking events for all /api calls.
    """

    def __call__(self, request):
        t_start = perf_counter()
        (request, requested_version, request_path_info) = self.process_request(request)

        # if there is CORS headers then assume the request is coming from the OrgBook app
        # (or the swagger page)
        internal_call = (
            "HTTP_SEC_FETCH_SITE" in request.META and
            request.META["HTTP_SEC_FETCH_SITE"] is not None and
            0 < len(request.META["HTTP_SEC_FETCH_SITE"])
        )
        req_parameters = []
        req_keys = {}
        if request.method == "GET":
            req_parms = request.GET.copy()
        elif request.method == "POST":
            req_parms = request.POST.copy()
        req_keys = req_parms.keys()
        for key in req_keys:
            if req_parms.get(key) and 0 < len(req_parms.get(key)):
                req_parameters.append(key)
        response = self.get_response(request)
        ret_response = self.process_response(request, response)
        t_stop = perf_counter()

        if self.track_metrics(request_path_info):
            if "url_endpoint" in ret_response:
                url_endpoint = ret_response["url_endpoint"]
            else:
                try:
                    url_match = resolve(request.path_info)
                except Exception:
                    url_match = None
                url_endpoint = url_match.route if url_match else request_path_info
                # fix up some common patterns that appear in django urls
                url_endpoint = url_endpoint.replace("$", "")
                url_endpoint = url_endpoint.replace("(?P<", "{")
                url_endpoint = url_endpoint.replace(">[^/.]+)", "}")
                url_endpoint = url_endpoint.replace(">[^/]+)", "}")
                url_endpoint = url_endpoint.replace("(<", "{")
                url_endpoint = url_endpoint.replace(">", "}")
            url_endpoint = url_endpoint.replace("/" + requested_version + "/", "/")
            item_count = int(ret_response["item_count"]) if "item_count" in ret_response else 1
            api_json = {
                'internal_call': internal_call,
                'api_version': requested_version,
                'endpoint': url_endpoint,
                'total': item_count,
                'response_time': t_stop-t_start,
                'parameters': req_parameters
            }
            tracker_json = SelfDescribingJson(
                'iglu:ca.bc.gov.orgbook/api_call/jsonschema/1-0-0',
                api_json
            )
            LOGGER.debug(f"API Tracking: {api_json}")
            settings.SP_TRACKER.track_self_describing_event(tracker_json)

        return ret_response

    def track_metrics(self, path_info):
        if path_info.startswith(settings.STATIC_URL):
            return False
        if path_info.startswith(settings.HTTP_HEADER_ROUTING_MIDDLEWARE_URL_FILTER):
            return True
        if path_info.startswith(settings.HTTP_AGENT_CALLBACK_MIDDLEWARE_URL_FILTER):
            # for now return False for agent callbacks
            return False
        # default return False (don't log metrics)
        return False
