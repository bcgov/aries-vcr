from drf_haystack.serializers import HaystackSerializerMixin, HaystackSerializer
from api.search_indexes import LocationIndex
from api.search_indexes import VODoingBusinessAsIndex
from api.search_indexes import VerifiedOrgIndex
from api.serializers import VODoingBusinessAsSerializer
from api.serializers import VerifiedOrgSerializer
from api.serializers import VOLocationSerializer

# -----------------------------------------------------------------------------------
# The Search serializers reuse the model serializers as shown here;
# - http://drf-haystack.readthedocs.io/en/latest/10_tips_n_tricks.html#reusing-model-serializers
#
# This will cause a database hit.  Refer to the warning on the above page.
# For now it is more convenient.
# -----------------------------------------------------------------------------------

class VerifiedOrgSearchSerializer(HaystackSerializerMixin, VerifiedOrgSerializer):
  class Meta (VerifiedOrgSerializer.Meta):
    search_fields = ("text", )    
    field_aliases = {}
    exclude = tuple()

class VODoingBusinessAsSearchSerializer(HaystackSerializerMixin, VODoingBusinessAsSerializer):
  class Meta (VODoingBusinessAsSerializer.Meta):
    search_fields = ("text", )    
    field_aliases = {}
    exclude = tuple()

class LocationSearchSerializer(HaystackSerializerMixin, VOLocationSerializer):
  class Meta (VOLocationSerializer.Meta):
    search_fields = ("text", )    
    field_aliases = {}
    exclude = tuple()

class NameSearchSerializer(HaystackSerializer):
  class Meta:
    search_fields = ("name", )    
    field_aliases = {}
    exclude = tuple()
    serializers = {
      VerifiedOrgIndex: VerifiedOrgSearchSerializer,
      VODoingBusinessAsIndex: VODoingBusinessAsSearchSerializer
    }

class OrganizationSearchSerializer(HaystackSerializer):
  class Meta:
    search_fields = ("text", )
    field_aliases = {}
    exclude = tuple()
    serializers = {
      VerifiedOrgIndex: VerifiedOrgSearchSerializer,
      VODoingBusinessAsIndex: VODoingBusinessAsSearchSerializer,
      LocationIndex: LocationSearchSerializer
    }
