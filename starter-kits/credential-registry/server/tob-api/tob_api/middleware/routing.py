import logging

from django.conf import settings

LOGGER = logging.getLogger(__name__)


class ApiVersionException(Exception):
    pass


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
        requested_version_header = None
        requested_version_path = None

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
                    raise ApiVersionException(
                        "Too many versions were specified in the Accept header."
                    )

                elif (
                    len(supported_version_headers) > 0
                    and "version=" in supported_version_headers[0]
                ):
                    # replace the ACCEPT header with a standard resource format,
                    # and record the requested version to use it later on
                    standard_content_header = supported_version_headers[0].split(";")[0]
                    requested_version_header = (
                        supported_version_headers[0]
                        .replace(standard_content_header, "")
                        .replace(";version=", "")
                    )

                    # ensure requested version is supported
                    if (
                        requested_version_header
                        not in settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP
                    ):
                        raise ApiVersionException(
                            f"The specified version [{requested_version_header}] is not supported."
                        )

                    LOGGER.debug(
                        f"Requested API version in Accept header is: '{requested_version_header}'"
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
            LOGGER.debug("Processing URL path to detect requested API version.")

            # check the URL path for supported version override
            for allowed_version in settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP:
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

                    requested_version_path = allowed_version
                    LOGGER.debug(
                        f"Requested API version in PATH header is: '{requested_version_path}'"
                    )

            if (
                requested_version_header is not None
                and requested_version_path is not None
                and requested_version_header != requested_version_path
            ):
                raise ApiVersionException(
                    f"Conflicting API versions were requested in Accept header [{requested_version_header}] and path [{requested_version_path}]."
                )
            elif requested_version_header is not None:
                requested_version = settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP[
                    requested_version_header
                ]
                LOGGER.debug(
                    f"Will be using API version specified in Accept header: [{requested_version}]"
                )
            elif requested_version_path is not None:
                requested_version = settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP[
                    requested_version_path
                ]
                LOGGER.debug(
                    f"Will be using API version specified in URL path: [{requested_version}]"
                )
            else:
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
