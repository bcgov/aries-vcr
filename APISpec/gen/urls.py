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
    url(r'^inactiveClaimReasons/bulk$', views.inactiveClaimReasonsBulkPost.as_view()),
    url(r'^inactiveClaimReasons$', views.inactiveClaimReasonsGet.as_view()),
    url(r'^inactiveClaimReasons/(?P<id>[0-9]+)/delete$', views.inactiveClaimReasonsIdDeletePost.as_view()),
    url(r'^inactiveClaimReasons/(?P<id>[0-9]+)$', views.inactiveClaimReasonsIdGet.as_view()),
    url(r'^issuerOrgs/bulk$', views.issuerOrgsBulkPost.as_view()),
    url(r'^issuerOrgs$', views.issuerOrgsGet.as_view()),
    url(r'^issuerOrgs/(?P<id>[0-9]+)/delete$', views.issuerOrgsIdDeletePost.as_view()),
    url(r'^issuerOrgs/(?P<id>[0-9]+)$', views.issuerOrgsIdGet.as_view()),
    url(r'^jurisdictions/bulk$', views.jurisdictionsBulkPost.as_view()),
    url(r'^jurisdictions$', views.jurisdictionsGet.as_view()),
    url(r'^jurisdictions/(?P<id>[0-9]+)/delete$', views.jurisdictionsIdDeletePost.as_view()),
    url(r'^jurisdictions/(?P<id>[0-9]+)$', views.jurisdictionsIdGet.as_view()),
    url(r'^voClaims/bulk$', views.voClaimsBulkPost.as_view()),
    url(r'^voClaims$', views.voClaimsGet.as_view()),
    url(r'^voClaims/(?P<id>[0-9]+)/delete$', views.voClaimsIdDeletePost.as_view()),
    url(r'^voClaims/(?P<id>[0-9]+)$', views.voClaimsIdGet.as_view()),
    url(r'^voClaimTypes/bulk$', views.voClaimTypesBulkPost.as_view()),
    url(r'^voClaimTypes$', views.voClaimTypesGet.as_view()),
    url(r'^voClaimTypes/(?P<id>[0-9]+)/delete$', views.voClaimTypesIdDeletePost.as_view()),
    url(r'^voClaimTypes/(?P<id>[0-9]+)$', views.voClaimTypesIdGet.as_view()),
    url(r'^voDoingBusinessAs/bulk$', views.voDoingBusinessAsBulkPost.as_view()),
    url(r'^voDoingBusinessAs$', views.voDoingBusinessAsGet.as_view()),
    url(r'^voDoingBusinessAs/(?P<id>[0-9]+)/delete$', views.voDoingBusinessAsIdDeletePost.as_view()),
    url(r'^voDoingBusinessAs/(?P<id>[0-9]+)$', views.voDoingBusinessAsIdGet.as_view()),
    url(r'^voLocations/bulk$', views.voLocationsBulkPost.as_view()),
    url(r'^voLocations$', views.voLocationsGet.as_view()),
    url(r'^voLocations/(?P<id>[0-9]+)/delete$', views.voLocationsIdDeletePost.as_view()),
    url(r'^voLocations/(?P<id>[0-9]+)$', views.voLocationsIdGet.as_view()),
    url(r'^voLocationTypes/bulk$', views.voLocationTypesBulkPost.as_view()),
    url(r'^voLocationTypes$', views.voLocationTypesGet.as_view()),
    url(r'^voLocationTypes/(?P<id>[0-9]+)/delete$', views.voLocationTypesIdDeletePost.as_view()),
    url(r'^voLocationTypes/(?P<id>[0-9]+)$', views.voLocationTypesIdGet.as_view()),
    url(r'^voOrgTypes/bulk$', views.voOrgTypesBulkPost.as_view()),
    url(r'^voOrgTypes$', views.voOrgTypesGet.as_view()),
    url(r'^voOrgTypes/(?P<id>[0-9]+)/delete$', views.voOrgTypesIdDeletePost.as_view()),
    url(r'^voOrgTypes/(?P<id>[0-9]+)$', views.voOrgTypesIdGet.as_view()),
    url(r'^verifiedOrgs/bulk$', views.verifiedOrgsBulkPost.as_view()),
    url(r'^verifiedOrgs$', views.verifiedOrgsGet.as_view()),
    url(r'^verifiedOrgs/(?P<id>[0-9]+)/delete$', views.verifiedOrgsIdDeletePost.as_view()),
    url(r'^verifiedOrgs/(?P<id>[0-9]+)$', views.verifiedOrgsIdGet.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
