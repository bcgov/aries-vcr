from rest_framework.mixins import ListModelMixin
from api.search_serializers import VODoingBusinessAsSearchSerializer
from api.models.VODoingBusinessAs import VODoingBusinessAs
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