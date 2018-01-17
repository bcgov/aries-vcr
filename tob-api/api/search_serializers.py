from drf_haystack.serializers import HaystackSerializerMixin, HaystackSerializer
from django.db.models.manager import Manager
from rest_framework.serializers import ListSerializer
from api.search_indexes import LocationIndex
from api.search_indexes import DoingBusinessAsIndex
from api.search_indexes import VerifiableOrgIndex
from api.serializers import DoingBusinessAsSerializer
from api.serializers import VerifiableOrgSerializer
from api.serializers import LocationSerializer
from collections import OrderedDict
from rest_framework.utils.serializer_helpers import ReturnDict

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

class SearchResultsListSerializer(ListSerializer):
  @staticmethod
  def __camelCase(s):
    return s[:1].lower() + s[1:] if s else ''

  def __get_keyName(self, instance):
    searchIndex = instance.searchindex
    model = searchIndex.get_model()
    return self.__camelCase(model.__name__)
  
  @property
  def data(self):
    ret = super(ListSerializer, self).data
    return ReturnDict(ret, serializer=self)  
    
  def to_representation(self, data):
    results = OrderedDict()
    iterable = data.all() if isinstance(data, Manager) else data
    for item in iterable:
      searchIndexName = self.__get_keyName(item)
      results.setdefault(searchIndexName, []).append(self.child.to_representation(item))

    return results

class NameSearchSerializer(HaystackSerializer):
  class Meta:
    list_serializer_class = SearchResultsListSerializer
    search_fields = ("name", )    
    field_aliases = {}
    exclude = tuple()
    serializers = {
      VerifiableOrgIndex: VerifiableOrgSearchSerializer,
      DoingBusinessAsIndex: DoingBusinessAsSearchSerializer
    }

class OrganizationSearchSerializer(HaystackSerializer):
  class Meta:
    list_serializer_class = SearchResultsListSerializer
    search_fields = ("text", )
    field_aliases = {}
    exclude = tuple()
    serializers = {
      VerifiableOrgIndex: VerifiableOrgSearchSerializer,
      DoingBusinessAsIndex: DoingBusinessAsSearchSerializer,
      LocationIndex: LocationSearchSerializer
    }
