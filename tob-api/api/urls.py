"""
    REST API Documentation for TheOrgBook

    TheOrgBook is a repository for Verifiable Claims made about Organizations related to a known foundational Verifiable Claim. See https://github.com/bcgov/VON

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
# search views
from . import search_views
# indy views
from . import indy_views

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

    url(r'^admin/records/counts', views_custom.recordCounts.as_view()),
    url(r'^quickload$', views_custom.quickLoad.as_view()),
    url(r'^settings$', views_custom.custom_settings.as_view()),

    url(r'^doingbusinessas/bulk$', views.doingbusinessasBulkPost.as_view()),
    url(r'^doingbusinessas$', views.doingbusinessasGet.as_view()),
    url(r'^doingbusinessas/(?P<id>[0-9]+)/delete$', views.doingbusinessasIdDeletePost.as_view()),
    url(r'^doingbusinessas/(?P<id>[0-9]+)$', views.doingbusinessasIdGet.as_view()),
    
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
    
    url(r'^locations/bulk$', views.locationsBulkPost.as_view()),
    url(r'^locations$', views.locationsGet.as_view()),
    url(r'^locations/(?P<id>[0-9]+)/delete$', views.locationsIdDeletePost.as_view()),
    url(r'^locations/(?P<id>[0-9]+)$', views.locationsIdGet.as_view()),

    url(r'^locationtypes/bulk$', views.locationtypesBulkPost.as_view()),
    url(r'^locationtypes$', views.locationtypesGet.as_view()),
    url(r'^locationtypes/(?P<id>[0-9]+)/delete$', views.locationtypesIdDeletePost.as_view()),
    url(r'^locationtypes/(?P<id>[0-9]+)$', views.locationtypesIdGet.as_view()),

    url(r'^verifiableclaims/bulk$', views.verifiableclaimsBulkPost.as_view()),
    url(r'^verifiableclaims$', views.verifiableclaimsGet.as_view()),
    url(r'^verifiableclaims/(?P<id>[0-9]+)/delete$', views.verifiableclaimsIdDeletePost.as_view()),
    url(r'^verifiableclaims/(?P<id>[0-9]+)$', views.verifiableclaimsIdGet.as_view()),
    url(r'^verifiableclaims/(?P<id>[0-9]+)/verify$', indy_views.bcovrinVerifyCredential.as_view()),

    url(r'^verifiableclaimtypes/bulk$', views.verifiableclaimtypesBulkPost.as_view()),
    url(r'^verifiableclaimtypes$', views.verifiableclaimtypesGet.as_view()),
    url(r'^verifiableclaimtypes/(?P<id>[0-9]+)/delete$', views.verifiableclaimtypesIdDeletePost.as_view()),
    url(r'^verifiableclaimtypes/(?P<id>[0-9]+)$', views.verifiableclaimtypesIdGet.as_view()),
    
    url(r'^verifiableorgs/bulk$', views.verifiableorgsBulkPost.as_view()),
    url(r'^verifiableorgs$', views.verifiableorgsGet.as_view()),
    url(r'^verifiableorgs/(?P<id>[0-9]+)/delete$', views.verifiableorgsIdDeletePost.as_view()),
    url(r'^verifiableorgs/(?P<id>[0-9]+)$', views.verifiableorgsIdGet.as_view()),
    url(r'^verifiableorgs/(?P<id>[0-9]+)/doingbusinessas$', views_custom.verifiableOrgsIdDoingBusinessAsGet.as_view()),
    url(r'^verifiableorgs/(?P<id>[0-9]+)/locations$', views_custom.verifiableOrgsIdLocationsGet.as_view()),
    url(r'^verifiableorgs/(?P<id>[0-9]+)/verifiableclaims$', views_custom.verifiableOrgsIdVerifiableclaimsGet.as_view()),
        
    url(r'^verifiableorgtypes/bulk$', views.verifiableorgtypesBulkPost.as_view()),
    url(r'^verifiableorgtypes$', views.verifiableorgtypesGet.as_view()),
    url(r'^verifiableorgtypes/(?P<id>[0-9]+)/delete$', views.verifiableorgtypesIdDeletePost.as_view()),
    url(r'^verifiableorgtypes/(?P<id>[0-9]+)$', views.verifiableorgtypesIdGet.as_view()),

    url(r'^search/doingbusinessas$', search_views.DoingBusinessAsSearchView.as_view()),
    url(r'^search/locations$', search_views.LocationSearchView.as_view()),
    url(r'^search/name$', search_views.NameSearchView.as_view()),
    url(r'^search/organization$', search_views.OrganizationSearchView.as_view()),
    url(r'^search/verifiableorgs$', search_views.VerifiableOrgSearchView.as_view()),

    url(r'^bcovrin/generate-claim-request$', indy_views.bcovrinGenerateClaimRequest.as_view()),
    url(r'^bcovrin/store-claim$', indy_views.bcovrinStoreClaim.as_view()),
    url(r'^bcovrin/construct-proof$', indy_views.bcovrinConstructProof.as_view()),
    url(r'^bcovrin/register-issuer$', indy_views.bcovrinRegisterIssuer.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
