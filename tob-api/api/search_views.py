from rest_framework.mixins import ListModelMixin
from api.search_serializers import OrganizationSearchSerializer
from api.search_serializers import NameSearchSerializer
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

class NameSearchView(ListModelMixin, HaystackGenericAPIView):
    index_models = [VerifiedOrg, VODoingBusinessAs]
    serializer_class = NameSearchSerializer
    def get(self, request, *args, **kwargs):
        """
        Searches across the 'name' fields of Verified Organization and 
        Doing Business As records.
        
        Returns any records that match the search criteria.

        Search field:
        - name

        Example:
        ```
        .../api/v1/name/search?name=gas
        ```

        Returns:
        ```
        [
            {
                "id": 8,
                "busId": "74905418",
                "orgTypeId": 1,
                "jurisdictionId": 1,
                "LegalName": "Gamma Gas",
                "effectiveDate": "2010-10-10",
                "endDate": null
            },
            {
                "id": 18,
                "verifiedOrgId": 8,
                "DBA": "Gas Depot",
                "effectiveDate": "2010-10-10",
                "endDate": null
            }
        ]
        ```
        """
        return self.list(request, *args, **kwargs)

class OrganizationSearchView(ListModelMixin, HaystackGenericAPIView):
    index_models = [VerifiedOrg, VODoingBusinessAs, VOLocation]
    serializer_class = OrganizationSearchSerializer
    def get(self, request, *args, **kwargs):
        """
        Searches across the text fields of Verified Organization, Doing Business As, and Location records.
        
        Returns any records that match the search criteria.

        Search field:
        - text

        Example:
        ```
        .../api/v1/organization/search?text=gas
        ```

        Returns:
        ```
        [
            {
                "id": 18,
                "verifiedOrgId": 8,
                "DBA": "Gas Depot",
                "effectiveDate": "2010-10-10",
                "endDate": null
            },
            {
                "id": 24,
                "verifiedOrgId": 8,
                "voLocationTypeId": 2,
                "addressee": "Gamma Gas",
                "addlDeliveryInfo": null,
                "unitNumber": null,
                "streetAddress": "735 Wallace Street",
                "municipality": "Nanaimo",
                "province": "BC",
                "postalCode": "V9R 3A8",
                "latLong": "49.108632, -123.871502",
                "effectiveDate": "2010-10-10",
                "endDate": null
            },
            {
                "id": 26,
                "verifiedOrgId": 8,
                "voLocationTypeId": 2,
                "addressee": "Gas Depot",
                "addlDeliveryInfo": null,
                "unitNumber": null,
                "streetAddress": "2890 Burdett Avenue",
                "municipality": "Victoria",
                "province": "BC",
                "postalCode": "V8Y 1Y7",
                "latLong": "48.415871, -123.392253",
                "effectiveDate": "2010-10-10",
                "endDate": null
            },
            {
                "id": 8,
                "busId": "74905418",
                "orgTypeId": 1,
                "jurisdictionId": 1,
                "LegalName": "Gamma Gas",
                "effectiveDate": "2010-10-10",
                "endDate": null
            }
        ]
        ```
        """
        return self.list(request, *args, **kwargs)