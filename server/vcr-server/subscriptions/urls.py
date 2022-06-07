from django.urls import path
from django.conf import settings

from subscriptions.views import (
    RegistrationCreateViewSet,
    RegistrationViewSet,
    SubscriptionViewSet,
)
from rest_framework.routers import SimpleRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.permissions import AllowAny

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from api.v2.swagger import HttpsSchemaGenerator

# see https://github.com/alanjds/drf-nested-routers
from rest_framework_nested import routers

app_name = "subscriptions"

API_METADATA = settings.API_METADATA
schema_view = get_schema_view(
    openapi.Info(
        title=API_METADATA["title"],
        description=API_METADATA["description"],
        default_version="v2",
        terms_of_service=API_METADATA["terms"]["url"],
        contact=openapi.Contact(**API_METADATA["contact"]),
        license=openapi.License(**API_METADATA["license"]),
    ),
    # url="{}/api".format(settings.APPLICATION_URL),
    validators=["flex", "ssv"],
    public=True,
    generator_class=HttpsSchemaGenerator,
    permission_classes=(AllowAny,),
)

router = SimpleRouter(trailing_slash=False)

# hook management (registration, add/update/delete hooks)
router.register(r"register", RegistrationCreateViewSet, "Web Hook Registration")
router.register(r"registration", RegistrationViewSet, "Web Hook Registration")
registrations_router = routers.NestedSimpleRouter(
    router, r"registration", lookup="registration"
)
registrations_router.register(
    r"subscriptions", SubscriptionViewSet, basename="subscriptions"
)


swaggerPatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=None), name="api-docs")
]

urlpatterns = (
    format_suffix_patterns(router.urls + registrations_router.urls) + swaggerPatterns
)
