### urls.py ###

from rest_framework import routers
from django.urls import path, include

from . import views

router = routers.SimpleRouter(trailing_slash=False)

urlpatterns = router.urls
urlpatterns.append(path('echo', views.echo_view, name='echo'))
urlpatterns.append(path('error', views.error_view, name='error'))
urlpatterns.append(path('rando', views.random_view, name='rando'))
