from drf_haystack.serializers import HaystackSerializerMixin, HaystackSerializer
from api.search_indexes import LocationIndex
from api.search_indexes import DoingBusinessAsIndex
from api.search_indexes import VerifiableOrgIndex
from api.serializers import DoingBusinessAsSerializer
from api.serializers import VerifiableOrgSerializer
from api.serializers import LocationSerializer

# -----------------------------------------------------------------------------------
# The Search serializers reuse the model serializers as shown here;
# - http://drf-haystack.readthedocs.io/en/latest/10_tips_n_tricks.html#reusing-model-serializers
#
# This will cause a database hit.  Refer to the warning on the above page.
# For now it is more convenient.
# -----------------------------------------------------------------------------------

class VerifiableOrgSearchSerializer(HaystackSerializerMixin, VerifiableOrgSerializer):
  class Meta (VerifiableOrgSerializer.Meta):
    search_fields = ("text", )    
    field_aliases = {}
    exclude = tuple()

class DoingBusinessAsSearchSerializer(HaystackSerializerMixin, DoingBusinessAsSerializer):
  class Meta (DoingBusinessAsSerializer.Meta):
    search_fields = ("text", )    
    field_aliases = {}
    exclude = tuple()

class LocationSearchSerializer(HaystackSerializerMixin, LocationSerializer):
  class Meta (LocationSerializer.Meta):
    search_fields = ("text", )    
    field_aliases = {}
    exclude = tuple()

class NameSearchSerializer(HaystackSerializer):
  class Meta:
    search_fields = ("name", )    
    field_aliases = {}
    exclude = tuple()
    serializers = {
      VerifiableOrgIndex: VerifiableOrgSearchSerializer,
      DoingBusinessAsIndex: DoingBusinessAsSearchSerializer
    }

class OrganizationSearchSerializer(HaystackSerializer):
  class Meta:
    search_fields = ("text", )
    field_aliases = {}
    exclude = tuple()
    serializers = {
      VerifiableOrgIndex: VerifiableOrgSearchSerializer,
      DoingBusinessAsIndex: DoingBusinessAsSearchSerializer,
      LocationIndex: LocationSearchSerializer
    }
