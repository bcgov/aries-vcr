"""
Definition of urls for app.
"""

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework.permissions import AllowAny

from django.conf import settings
from django.urls import include, path
from django.views.generic import RedirectView

from . import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

API_METADATA = settings.API_METADATA
schema_view = get_schema_view(
    openapi.Info(
        title=API_METADATA["title"],
        description=API_METADATA["description"],
        default_version="v3",
        terms_of_service=API_METADATA["terms"]["url"],
        contact=openapi.Contact(**API_METADATA["contact"]),
        license=openapi.License(**API_METADATA["license"]),
    ),
    # url="{}/api".format(settings.APPLICATION_URL),
    validators=["flex", "ssv"],
    public=True,
    permission_classes=(AllowAny,),
)


base_patterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("health", views.health),
]

hook_patterns = [
    path("hooks/", include("subscriptions.urls"), name="subscriptions"),
    path("agentcb/", include("agent_webhooks.urls"), name="agent-callback"),
]

api_patterns = [
    path("", RedirectView.as_view(url="api/"), name="api-root"),
    path("api", RedirectView.as_view(url="api/"), name="api"),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=None), name="api-docs"),
    path("api/v2/", include("api.v2.urls"), name="api-v2"),
    path("api/v3/", include("api.v3.urls"), name="api-v3"),
]

urlpatterns = base_patterns + hook_patterns + api_patterns
