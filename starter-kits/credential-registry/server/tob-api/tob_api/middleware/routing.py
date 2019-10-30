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
        header_version = None
        header_meta = None
        path_version = None
        request_path_info = request.path_info

        # only process for API calls
        if request.path_info.startswith(
            settings.HTTP_HEADER_ROUTING_MIDDLEWARE_URL_FILTER + "/"
        ):
            # check Accept header for supported version override
            LOGGER.debug("Processing request headers to detect requested API version.")
            header_version, header_meta = self.extract_header_version(request)

            # check the URL path for supported version override
            LOGGER.debug("Processing URL to detect requested API version.")
            path_version, request_path_info = self.extract_path_version(request)

            # pick the right version to be used
            requested_version = self.get_coalesced_request_version(
                header_version, path_version
            )

            # replace accept headers with standard content header
            if header_meta is not None:
                request.META["HTTP_ACCEPT"] = header_meta

            # rewrite the requested version into the path
            request.path_info = request_path_info.replace(
                "api/", f"api/{requested_version}/"
            )

            LOGGER.debug(f"Resolved API url is {request.path_info}")

            return request

    def process_response(self, request, response):
        return response

    def extract_header_version(self, request):
        header_version = None
        request_meta_accept = request.META["HTTP_ACCEPT"]

        if "HTTP_ACCEPT" in request.META:
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
                header_content = supported_version_headers[0].split(";")[0]
                header_version = (
                    supported_version_headers[0]
                    .replace(header_content, "")
                    .replace(";version=", "")
                )

                # ensure requested version is supported
                if (
                    header_version
                    not in settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP
                ):
                    raise ApiVersionException(
                        f"The specified version [{header_version}] is not supported."
                    )

                LOGGER.debug(
                    f"Requested API version in Accept header is: '{header_version}'"
                )

                accept_headers[:] = [
                    header_content if x == supported_version_headers[0] else x
                    for x in accept_headers
                ]

                # re-construct header
                request_meta_accept = ",".join(accept_headers)

                return header_version, request_meta_accept

    def extract_path_version(self, request):
        path_version = None
        request_path_info = None

        for allowed_version in settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP:
            if request.path_info.startswith(
                settings.HTTP_HEADER_ROUTING_MIDDLEWARE_URL_FILTER
                + "/"
                + allowed_version
                + "/"
            ):
                # remove version info from the path (we will inject it later)
                request_path_info = request_path_info.replace(
                    f"/{allowed_version}/", "/"
                )

                path_version = allowed_version
                LOGGER.debug(
                    f"Requested API version in PATH header is: '{path_version}'"
                )

        return path_version, request_path_info

    def get_coalesced_request_version(self, header_version, path_version):
        use_version = None

        if header_version is None and path_version is None:
            LOGGER.debug("No version override detected, will be using 'default")
            use_version = settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP["default"]
        elif header_version != path_version:
            raise ApiVersionException(
                f"Conflicting API versions were requested in Accept header [{header_version}] and path [{path_version}]."
            )
        elif header_version is not None:
            LOGGER.debug(
                f"Will be using API version specified in Accept header: [{header_version}]"
            )
            use_version = settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP[
                header_version
            ]
        elif path_version is not None:
            LOGGER.debug(
                f"Will be using API version specified in URL path: [{path_version}]"
            )
            use_version = settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP[
                path_version
            ]

        return use_version
