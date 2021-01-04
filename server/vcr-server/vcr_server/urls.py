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


base_patterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("health", views.health),
]

hook_patterns = [
    path(
        "hooks/",
        include("subscriptions.urls", namespace="subscriptions"),
        name="subscriptions",
    ),
    path("agentcb/", include("agent_webhooks.urls"), name="agent-callback"),
]

api_patterns = [
    path("", RedirectView.as_view(url="api/"), name="api-root"),
    path("api", RedirectView.as_view(url="api/"), name="api"),
    path("api/v2/", include("api.v2.urls", namespace="v2"), name="api-v2"),
    path("api/v3/", include("api.v3.urls", namespace="v3"), name="api-v3"),
    path("api/v4/", include("api.v4.urls", namespace="v4"), name="api-v4"),
]

urlpatterns = base_patterns + hook_patterns + api_patterns
