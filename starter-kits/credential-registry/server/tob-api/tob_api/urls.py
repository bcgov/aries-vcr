"""
Definition of urls for tob_api.
"""

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
    path("hooks/", include("icat_hooks.urls")),
    path("agentcb/", include("icat_cbs.urls")),
]

api_patterns = [
    path("", RedirectView.as_view(url="api/")),
    path("api/v2/", include("api_v2.urls")),
]

urlpatterns = base_patterns + hook_patterns + api_patterns
