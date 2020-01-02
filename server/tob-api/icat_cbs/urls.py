from django.conf import settings
from django.urls import path

from icat_cbs import views, views_debug

urlpatterns = [path("topic/<topic>/", views.agent_callback)]

# expose debug APIs if in debug mode 
if settings.DEBUG:
    urlpatterns.append(path("debug/receive-credential/", views_debug.receive_credential))
