import datetime
from api.models.DoingBusinessAs import DoingBusinessAs
from api.models.VerifiableOrg import VerifiableOrg
from api.models.Location import Location
from haystack import indexes
from django.utils import timezone

class VerifiableOrgIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    orgId = indexes.CharField(model_attr="orgId")
    legalName = indexes.CharField(model_attr="legalName")
    name = indexes.CharField(model_attr="legalName")
    
    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.orgId,
            obj.legalName,
        ))

    def get_model(self):
        return VerifiableOrg

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            CREATE_TIMESTAMP__lte=timezone.now()
        )

class DoingBusinessAsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    dbaName = indexes.CharField(model_attr="dbaName")
    name = indexes.CharField(model_attr="dbaName")

    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.dbaName,
        ))

    def get_model(self):
        return DoingBusinessAs

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            CREATE_TIMESTAMP__lte=timezone.now()
        )

class LocationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    addressee = indexes.CharField(model_attr="addressee")
    municipality = indexes.CharField(model_attr="municipality")
    postalCode = indexes.CharField(model_attr="postalCode")
    province = indexes.CharField(model_attr="province")
    streetAddress = indexes.CharField(model_attr="streetAddress")

    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.addressee,
            obj.municipality,
            obj.postalCode,
            obj.province,
            obj.streetAddress,
        ))

    def get_model(self):
        return Location

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            CREATE_TIMESTAMP__lte=timezone.now()
        )