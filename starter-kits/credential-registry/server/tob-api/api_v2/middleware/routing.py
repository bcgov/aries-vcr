from django.conf import settings


class HTTPHeaderRoutingMiddleware(object):
    """
    Middleware to inject the API version into the API's URL.  The version can be supplied in the URL, or in api-name
    Accept request header.  Allowable header and version values are in settings.HTTP_HEADER_ROUTING_MIDDLEWARE_ACCEPT_MAP
    and settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP respectively.

    If there is a version requested in the Accept header it will use it, 
    else if there is a version requested in the URL it will use it,
    else it will use the version identified as "default".

    The Accept header (if supplied) will be rewritted as a regular content header (as mapped in settings) and the 
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
        # only process for API calls
        if request.path_info.startswith(settings.HTTP_HEADER_ROUTING_MIDDLEWARE_URL_FILTER + "/"):
            # check the ACCEPT header for version override
            version = None
            if 'HTTP_ACCEPT' in request.META:
                for content_type in settings.HTTP_HEADER_ROUTING_MIDDLEWARE_ACCEPT_MAP:
                    if (request.META['HTTP_ACCEPT'].find(content_type) != -1):
                        # replace the ACCEPT header with a standard resource format
                        accept_header = request.META['HTTP_ACCEPT']
                        request.META['HTTP_ACCEPT'] = settings.HTTP_HEADER_ROUTING_MIDDLEWARE_ACCEPT_MAP[content_type]

                        # parse out version number (if available)
                        idx = accept_header.find("version=")
                        if 0 <= idx:
                            version = accept_header[idx+len("version="):].lower()

            # if there is a version requested in the path, use it
            request_path_info = request.path_info
            for allowed_version in settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP:
                if request_path_info.startswith(settings.HTTP_HEADER_ROUTING_MIDDLEWARE_URL_FILTER + "/" + allowed_version + "/"):
                    # remove version info from the path (we will inject it later)
                    request_path_info = settings.HTTP_HEADER_ROUTING_MIDDLEWARE_URL_FILTER + "/" + request_path_info[len(settings.HTTP_HEADER_ROUTING_MIDDLEWARE_URL_FILTER + "/" + allowed_version + "/"):]
                    if not version:
                        version = allowed_version

            # use the default version if none is specified
            if not version:
                version = settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP["default"]

            # check for a valid version
            use_version = None
            for allowed_version in settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP:
                if version == allowed_version:
                    use_version = settings.HTTP_HEADER_ROUTING_MIDDLEWARE_VERSION_MAP[version]
            if not use_version:
                return
            
            # rewrite the requested version into the path
            request.path_info = settings.HTTP_HEADER_ROUTING_MIDDLEWARE_URL_FILTER + "/" + use_version + request_path_info[len(settings.HTTP_HEADER_ROUTING_MIDDLEWARE_URL_FILTER):]


    def process_response(self, request, response):
        return response
