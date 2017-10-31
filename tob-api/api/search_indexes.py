import datetime
from api.models.VODoingBusinessAs import VODoingBusinessAs
from api.models.VerifiedOrg import VerifiedOrg
from api.models.VOLocation import VOLocation
from haystack import indexes
from django.utils import timezone

class VerifiedOrgIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    busId = indexes.CharField(model_attr="busId")
    LegalName = indexes.CharField(model_attr="LegalName")
    name = indexes.CharField(model_attr="LegalName")
    
    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.busId,
            obj.LegalName,
        ))

    def get_model(self):
        return VerifiedOrg

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            CREATE_TIMESTAMP__lte=timezone.now()
        )

class VODoingBusinessAsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    DBA = indexes.CharField(model_attr="DBA")
    name = indexes.CharField(model_attr="DBA")

    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.DBA,
        ))

    def get_model(self):
        return VODoingBusinessAs

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
        return VOLocation

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            CREATE_TIMESTAMP__lte=timezone.now()
        )