import logging

from django.conf import settings
from django.http import HttpResponseBadRequest

LOGGER = logging.getLogger(__name__)


class HTTPHeaderRoutingMiddleware(object):
    """
    Middleware to inject the API version into the API's URL.  The version can be supplied in the URL, or in api-name
    Accept request header.  Allowable header and version values are in settings.HTTP_HEADER_ROUTING_MIDDLEWARE_ACCEPT_MAP
    and settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP respectively.

    If there is a version requested in the Accept header it will be used, 
    else if there is a version requested in the URL it will be used,
    else it will use the version identified as "default".

    The Accept header (if supplied) will be rewritten as a regular content header (as mapped in settings) and the 
    version written into the URL will be as mapped in the settings.

    The actual API URL's must be mapped under "/api/v2/...", "/api/v3/..." etc. in the Django urlconf files.

    For example:
    `curl http://localhost:8081/api/credential` = uses the default version
    `curl http://localhost:8081/api/default/credential` = uses the default version
    `curl http://localhost:8081/api/v2/credential` = uses explicit version v2
    `curl --header "Accept: application/orgbook.bc.api+json" http://localhost:8081/api/credential` = uses the default version
    `curl --header "Accept: application/orgbook.bc.api+json; version=latest" http://localhost:8081/api/credential` = uses the latest version
    `curl --header "Accept: application/orgbook.bc.api+json; version=v2" http://localhost:8081/api/credential` = uses explicit version v2
    `curl --header "Accept: application/orgbook.bc.api+json; version=v2" http://localhost:8081/api/default/credential` = uses explicit version v2 (Accept header taked precidence)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)

        response = self.get_response(request)

        return self.process_response(request, response)

    def process_request(self, request):
        requested_version = None

        # only process for API calls
        if request.path_info.startswith(
            settings.HTTP_HEADER_ROUTING_MIDDLEWARE_URL_FILTER + "/"
        ):
            # check the ACCEPT header for version override
            if "HTTP_ACCEPT" in request.META:
                LOGGER.debug(
                    "Processing Accept headers to detect requested API version."
                )

                accept_headers = request.META["HTTP_ACCEPT"].split(",")
                accept_headers = list(map(lambda item: item.strip(), accept_headers))

                # find supported header definitions
                supported_version_headers = list(
                    filter(
                        lambda item: item.split(";")[0]
                        in settings.HTTP_HEADER_ROUTING_MIDDLEWARE_ACCEPT_MAP.values(),
                        accept_headers,
                    )
                )

                if len(supported_version_headers) > 1:
                    # Return error if more than one supported version is specified
                    return HttpResponseBadRequest(
                        content="Too many versions were specified in the Accept header."
                    )

                if "version=" in supported_version_headers[0]:
                    # replace the ACCEPT header with a standard resource format,
                    # and record the requested version to use it later on
                    standard_content_header = supported_version_headers[0].split(
                        ";"
                    )[0]
                    requested_version = (
                        supported_version_headers[0]
                        .replace(standard_content_header, "")
                        .replace(";version=", "")
                    )

                    # ensure requested version is supported
                    if (
                        requested_version
                        not in settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP
                    ):
                        return HttpResponseBadRequest(
                            content=f"The specified version [{requested_version}] is not supported."
                        )

                    LOGGER.debug(
                        f"Requested API version in Accept header is: '{requested_version}'"
                    )

                    accept_headers[:] = [
                        standard_content_header
                        if x == supported_version_headers[0]
                        else x
                        for x in accept_headers
                    ]

                    # re-construct header
                    request.META["HTTP_ACCEPT"] = ",".join(accept_headers)

            request_path_info = request.path_info
            if requested_version is None:
                LOGGER.debug("Processing URL path to detect requested API version.")

                # check the URL path for supported version override
                for (
                    allowed_version
                ) in settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP:
                    if request_path_info.startswith(
                        settings.HTTP_HEADER_ROUTING_MIDDLEWARE_URL_FILTER
                        + "/"
                        + allowed_version
                        + "/"
                    ):
                        # remove version info from the path (we will inject it later)
                        request_path_info = request_path_info.replace(
                            f"/{allowed_version}/", "/"
                        )

                        requested_version = allowed_version
                        LOGGER.debug(
                            f"Requested API version in PATH header is: '{requested_version}'"
                        )

            # use the default version if none is specified
            if requested_version is None:
                requested_version = settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP[
                    "default"
                ]
                LOGGER.debug("No version override detected, will be using 'default")

            # rewrite the requested version into the path
            request.path_info = request_path_info.replace(
                "api/", f"api/{requested_version}/"
            )

            LOGGER.debug(f"Resolved API url is {request.path_info}")

            return request

    def process_response(self, request, response):
        return response
