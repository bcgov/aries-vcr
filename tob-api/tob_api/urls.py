"""
Definition of urls for tob_api.
"""

from django.conf.urls import include, url
from django.views.generic import RedirectView
from . import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    url(r"^$", RedirectView.as_view(url="api/v2/")),
    url(
        r"^api-auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
    url(r"^api/v2/", include("api_v2.urls")),
    url(r"^health$", views.health),
]
