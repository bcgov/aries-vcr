from rest_framework.mixins import ListModelMixin
from api.search_serializers import VOTypeSearchSerializer
from api.models.VOType import VOType
from api.search_serializers import VOLocationTypeSearchSerializer
from api.models.VOLocationType import VOLocationType
from api.search_serializers import VODoingBusinessAsSearchSerializer
from api.models.VODoingBusinessAs import VODoingBusinessAs
from api.search_serializers import VOClaimTypeSearchSerializer
from api.models.VOClaimType import VOClaimType
from api.search_serializers import JurisdictionSearchSerializer
from api.models.Jurisdiction import Jurisdiction
from api.search_serializers import IssuerServiceSearchSerializer
from api.models.IssuerService import IssuerService
from api.search_serializers import InactiveClaimReasonSearchSerializer
from api.models.InactiveClaimReason import InactiveClaimReason
from drf_haystack.generics import HaystackGenericAPIView
from api.models.VerifiedOrg import VerifiedOrg
from api.models.VOLocation import VOLocation
from api.search_serializers import VerifiedOrgSearchSerializer
from api.search_serializers import LocationSearchSerializer

# -----------------------------------------------------------------------------------
# The Search Views use the simplified implementation shown here;
# - http://drf-haystack.readthedocs.io/en/latest/10_tips_n_tricks.html#regular-search-view
#
# The alternate implementation uses a HaystackViewSet containing additional 
# bells and whistles, but requires a router for URL configuration;
# - http://drf-haystack.readthedocs.io/en/latest/01_intro.html
# -----------------------------------------------------------------------------------
class InactiveClaimReasonSearchView(ListModelMixin, HaystackGenericAPIView):
    index_models = [InactiveClaimReason]
    serializer_class = InactiveClaimReasonSearchSerializer
    def get(self, request, *args, **kwargs):
        """
        Provides basic search capabilities.
        For more information refer to [drf-haystack](http://drf-haystack.readthedocs.io/en/latest/)

        Searchable fields:
        - reason
        - shortReason
        """
        return self.list(request, *args, **kwargs)

class IssuerServiceSearchView(ListModelMixin, HaystackGenericAPIView):
    index_models = [IssuerService]
    serializer_class = IssuerServiceSearchSerializer
    def get(self, request, *args, **kwargs):
        """
        Provides basic search capabilities.
        For more information refer to [drf-haystack](http://drf-haystack.readthedocs.io/en/latest/)

        Searchable fields:
        - name
        - issuerOrgTLA
        """
        return self.list(request, *args, **kwargs)

class JurisdictionSearchView(ListModelMixin, HaystackGenericAPIView):
    index_models = [Jurisdiction]
    serializer_class = JurisdictionSearchSerializer
    def get(self, request, *args, **kwargs):
        """
        Provides basic search capabilities.
        For more information refer to [drf-haystack](http://drf-haystack.readthedocs.io/en/latest/)

        Searchable fields:
        - name
        - abbrv
        """
        return self.list(request, *args, **kwargs)

class VerifiedOrgSearchView(ListModelMixin, HaystackGenericAPIView):
    index_models = [VerifiedOrg]
    serializer_class = VerifiedOrgSearchSerializer
    def get(self, request, *args, **kwargs):
        """
        Provides basic search capabilities.
        For more information refer to [drf-haystack](http://drf-haystack.readthedocs.io/en/latest/)

        Searchable fields:
        - busId
        - LegalName
        """
        return self.list(request, *args, **kwargs)

class VOClaimTypeSearchView(ListModelMixin, HaystackGenericAPIView):
    index_models = [VOClaimType]
    serializer_class = VOClaimTypeSearchSerializer
    def get(self, request, *args, **kwargs):
        """
        Provides basic search capabilities.
        For more information refer to [drf-haystack](http://drf-haystack.readthedocs.io/en/latest/)

        Searchable fields:
        - theType
        """
        return self.list(request, *args, **kwargs)

class VODoingBusinessAsSearchView(ListModelMixin, HaystackGenericAPIView):
    index_models = [VODoingBusinessAs]
    serializer_class = VODoingBusinessAsSearchSerializer
    def get(self, request, *args, **kwargs):
        """
        Provides basic search capabilities.
        For more information refer to [drf-haystack](http://drf-haystack.readthedocs.io/en/latest/)

        Searchable fields:
        - DBA
        """
        return self.list(request, *args, **kwargs)

class LocationSearchView(ListModelMixin, HaystackGenericAPIView):
    index_models = [VOLocation]
    serializer_class = LocationSearchSerializer
    def get(self, request, *args, **kwargs):
        """
        Provides basic search capabilities.
        For more information refer to [drf-haystack](http://drf-haystack.readthedocs.io/en/latest/)

        Searchable fields:
        - addressee
        - municipality
        - postalCode
        - province
        - streetAddress
        """
        return self.list(request, *args, **kwargs)

class VOLocationTypeSearchView(ListModelMixin, HaystackGenericAPIView):
    index_models = [VOLocationType]
    serializer_class = VOLocationTypeSearchSerializer
    def get(self, request, *args, **kwargs):
        """
        Provides basic search capabilities.
        For more information refer to [drf-haystack](http://drf-haystack.readthedocs.io/en/latest/)

        Searchable fields:
        - theType
        - description
        """
        return self.list(request, *args, **kwargs)

class VOTypeSearchView(ListModelMixin, HaystackGenericAPIView):
    index_models = [VOType]
    serializer_class = VOTypeSearchSerializer
    def get(self, request, *args, **kwargs):
        """
        Provides basic search capabilities.
        For more information refer to [drf-haystack](http://drf-haystack.readthedocs.io/en/latest/)

        Searchable fields:
        - theType
        - description
        """
        return self.list(request, *args, **kwargs)