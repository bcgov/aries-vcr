from drf_haystack.serializers import HaystackSerializerMixin
from api.serializers import VOTypeSerializer
from api.serializers import VOLocationTypeSerializer
from api.serializers import VODoingBusinessAsSerializer
from api.serializers import VOClaimTypeSerializer
from api.serializers import JurisdictionSerializer
from api.serializers import IssuerServiceSerializer
from api.serializers import InactiveClaimReasonSerializer
from api.serializers import VerifiedOrgSerializer
from api.serializers import VOLocationSerializer

# -----------------------------------------------------------------------------------
# The Search serializers reuse the model serializers as shown here;
# - http://drf-haystack.readthedocs.io/en/latest/10_tips_n_tricks.html#reusing-model-serializers
#
# This will cause a database hit.  Refer to the warning on the above page.
# For now it is more convenient.
# -----------------------------------------------------------------------------------

class InactiveClaimReasonSearchSerializer(HaystackSerializerMixin, InactiveClaimReasonSerializer):
  class Meta (InactiveClaimReasonSerializer.Meta):
    search_fields = ("text", )    
    field_aliases = {}
    exclude = tuple()

class IssuerServiceSearchSerializer(HaystackSerializerMixin, IssuerServiceSerializer):
  class Meta (IssuerServiceSerializer.Meta):
    search_fields = ("text", )    
    field_aliases = {}
    exclude = tuple()

class JurisdictionSearchSerializer(HaystackSerializerMixin, JurisdictionSerializer):
  class Meta (JurisdictionSerializer.Meta):
    search_fields = ("text", )    
    field_aliases = {}
    exclude = tuple()

class VerifiedOrgSearchSerializer(HaystackSerializerMixin, VerifiedOrgSerializer):
  class Meta (VerifiedOrgSerializer.Meta):
    search_fields = ("text", )    
    field_aliases = {}
    exclude = tuple()

class VOClaimTypeSearchSerializer(HaystackSerializerMixin, VOClaimTypeSerializer):
  class Meta (VOClaimTypeSerializer.Meta):
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

class VOLocationTypeSearchSerializer(HaystackSerializerMixin, VOLocationTypeSerializer):
  class Meta (VOLocationTypeSerializer.Meta):
    search_fields = ("text", )    
    field_aliases = {}
    exclude = tuple()

class VOTypeSearchSerializer(HaystackSerializerMixin, VOTypeSerializer):
  class Meta (VOTypeSerializer.Meta):
    search_fields = ("text", )    
    field_aliases = {}
    exclude = tuple()