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
    url(r'^$', RedirectView.as_view(url='api/v1/')),
    url(r'^api/v1/quickload', views.quickload),
    url(r'^api/v1/', include('api.urls')),
    url(r'^health$', views.health),
]
