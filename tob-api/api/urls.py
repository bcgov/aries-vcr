"""
    REST API Documentation for TheOrgBook

    TheOrgBook is a repository for Verified Claims made about Organizations related to a known foundational Verified Claim. See https://github.com/bcgov/VON

    OpenAPI spec version: v1
        

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from django.conf.urls import url
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger import renderers
# generated views
from . import views
# custom views
from . import views_custom

class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]
    _ignore_model_permissions = True
    exclude_from_schema = True  
    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)
        return Response(schema)

urlpatterns = [
    # Swagger documentation
    url(r'^$', SwaggerSchemaView.as_view()),
    url(r'^users/current$', views_custom.usersCurrentGet.as_view()),
    url(r'^inactiveclaimreasons/bulk$', views.inactiveclaimreasonsBulkPost.as_view()),
    url(r'^inactiveclaimreasons$', views.inactiveclaimreasonsGet.as_view()),
    url(r'^inactiveclaimreasons/(?P<id>[0-9]+)/delete$', views.inactiveclaimreasonsIdDeletePost.as_view()),
    url(r'^inactiveclaimreasons/(?P<id>[0-9]+)$', views.inactiveclaimreasonsIdGet.as_view()),
    url(r'^issuerservices/bulk$', views.issuerservicesBulkPost.as_view()),
    url(r'^issuerservices$', views.issuerservicesGet.as_view()),
    url(r'^issuerservices/(?P<id>[0-9]+)/delete$', views.issuerservicesIdDeletePost.as_view()),
    url(r'^issuerservices/(?P<id>[0-9]+)$', views.issuerservicesIdGet.as_view()),
    url(r'^jurisdictions/bulk$', views.jurisdictionsBulkPost.as_view()),
    url(r'^jurisdictions$', views.jurisdictionsGet.as_view()),
    url(r'^jurisdictions/(?P<id>[0-9]+)/delete$', views.jurisdictionsIdDeletePost.as_view()),
    url(r'^jurisdictions/(?P<id>[0-9]+)$', views.jurisdictionsIdGet.as_view()),
    url(r'^permissions/bulk$', views.permissionsBulkPost.as_view()),
    url(r'^permissions$', views.permissionsGet.as_view()),
    url(r'^permissions/(?P<id>[0-9]+)/delete$', views.permissionsIdDeletePost.as_view()),
    url(r'^permissions/(?P<id>[0-9]+)$', views.permissionsIdGet.as_view()),
    url(r'^roles/bulk$', views.rolesBulkPost.as_view()),
    url(r'^roles$', views.rolesGet.as_view()),
    url(r'^roles/(?P<id>[0-9]+)/delete$', views.rolesIdDeletePost.as_view()),
    url(r'^roles/(?P<id>[0-9]+)$', views.rolesIdGet.as_view()),
    url(r'^roles/(?P<id>[0-9]+)/permissions$', views_custom.rolesIdPermissionsGet.as_view()),
    url(r'^roles/(?P<id>[0-9]+)/users$', views_custom.rolesIdUsersGet.as_view()),
    url(r'^rolepermissions/bulk$', views.rolepermissionsBulkPost.as_view()),
    url(r'^rolepermissions$', views.rolepermissionsGet.as_view()),
    url(r'^rolepermissions/(?P<id>[0-9]+)/delete$', views.rolepermissionsIdDeletePost.as_view()),
    url(r'^rolepermissions/(?P<id>[0-9]+)$', views.rolepermissionsIdGet.as_view()),
    url(r'^users/bulk$', views.usersBulkPost.as_view()),
    url(r'^users$', views.usersGet.as_view()),
    url(r'^users/(?P<id>[0-9]+)/delete$', views.usersIdDeletePost.as_view()),
    url(r'^users/(?P<id>[0-9]+)$', views.usersIdGet.as_view()),
    url(r'^users/(?P<id>[0-9]+)/permissions$', views_custom.usersIdPermissionsGet.as_view()),
    url(r'^users/(?P<id>[0-9]+)/roles$', views_custom.usersIdRolesGet.as_view()),
    url(r'^users/search$', views_custom.usersSearchGet.as_view()),
    url(r'^userroles/bulk$', views.userrolesBulkPost.as_view()),
    url(r'^userroles$', views.userrolesGet.as_view()),
    url(r'^userroles/(?P<id>[0-9]+)/delete$', views.userrolesIdDeletePost.as_view()),
    url(r'^userroles/(?P<id>[0-9]+)$', views.userrolesIdGet.as_view()),
    url(r'^voclaims/bulk$', views.voclaimsBulkPost.as_view()),
    url(r'^voclaims$', views.voclaimsGet.as_view()),
    url(r'^voclaims/(?P<id>[0-9]+)/delete$', views.voclaimsIdDeletePost.as_view()),
    url(r'^voclaims/(?P<id>[0-9]+)$', views.voclaimsIdGet.as_view()),
    url(r'^voclaimtypes/bulk$', views.voclaimtypesBulkPost.as_view()),
    url(r'^voclaimtypes$', views.voclaimtypesGet.as_view()),
    url(r'^voclaimtypes/(?P<id>[0-9]+)/delete$', views.voclaimtypesIdDeletePost.as_view()),
    url(r'^voclaimtypes/(?P<id>[0-9]+)$', views.voclaimtypesIdGet.as_view()),
    url(r'^vodoingbusinessas/bulk$', views.vodoingbusinessasBulkPost.as_view()),
    url(r'^vodoingbusinessas$', views.vodoingbusinessasGet.as_view()),
    url(r'^vodoingbusinessas/(?P<id>[0-9]+)/delete$', views.vodoingbusinessasIdDeletePost.as_view()),
    url(r'^vodoingbusinessas/(?P<id>[0-9]+)$', views.vodoingbusinessasIdGet.as_view()),
    url(r'^volocations/bulk$', views.volocationsBulkPost.as_view()),
    url(r'^volocations$', views.volocationsGet.as_view()),
    url(r'^volocations/(?P<id>[0-9]+)/delete$', views.volocationsIdDeletePost.as_view()),
    url(r'^volocations/(?P<id>[0-9]+)$', views.volocationsIdGet.as_view()),
    url(r'^volocationtypes/bulk$', views.volocationtypesBulkPost.as_view()),
    url(r'^volocationtypes$', views.volocationtypesGet.as_view()),
    url(r'^volocationtypes/(?P<id>[0-9]+)/delete$', views.volocationtypesIdDeletePost.as_view()),
    url(r'^volocationtypes/(?P<id>[0-9]+)$', views.volocationtypesIdGet.as_view()),
    url(r'^voorgtypes/bulk$', views.voorgtypesBulkPost.as_view()),
    url(r'^voorgtypes$', views.voorgtypesGet.as_view()),
    url(r'^voorgtypes/(?P<id>[0-9]+)/delete$', views.voorgtypesIdDeletePost.as_view()),
    url(r'^voorgtypes/(?P<id>[0-9]+)$', views.voorgtypesIdGet.as_view()),
    url(r'^verifiedorgs/bulk$', views.verifiedorgsBulkPost.as_view()),
    url(r'^verifiedorgs$', views.verifiedorgsGet.as_view()),
    url(r'^verifiedorgs/(?P<id>[0-9]+)/delete$', views.verifiedorgsIdDeletePost.as_view()),
    url(r'^verifiedorgs/(?P<id>[0-9]+)$', views.verifiedorgsIdGet.as_view()),
    url(r'^verifiedorgs/(?P<id>[0-9]+)/voclaims$', views_custom.verifiedorgsIdVoclaimsGet.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
