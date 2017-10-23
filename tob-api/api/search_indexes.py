import datetime
from api.models.VOType import VOType
from api.models.VOLocationType import VOLocationType
from api.models.VODoingBusinessAs import VODoingBusinessAs
from api.models.VOClaimType import VOClaimType
from api.models.VOClaim import VOClaim
from api.models.Jurisdiction import Jurisdiction
from api.models.InactiveClaimReason import InactiveClaimReason
from api.models.IssuerService import IssuerService
from api.models.VerifiedOrg import VerifiedOrg
from api.models.VOLocation import VOLocation
from haystack import indexes
from django.utils import timezone

class InactiveClaimReasonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    reason = indexes.CharField(model_attr="reason")
    shortReason = indexes.CharField(model_attr="shortReason")

    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.reason,
            obj.shortReason,
        ))

    def get_model(self):
        return InactiveClaimReason

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            CREATE_TIMESTAMP__lte=timezone.now()
        )

class IssuerServiceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")
    issuerOrgTLA = indexes.CharField(model_attr="issuerOrgTLA")

    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.name,
            obj.issuerOrgTLA,
        ))

    def get_model(self):
        return IssuerService

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            CREATE_TIMESTAMP__lte=timezone.now()
        )

class JurisdictionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")
    abbrv = indexes.CharField(model_attr="abbrv")

    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.name,
            obj.abbrv,
        ))

    def get_model(self):
        return Jurisdiction

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            CREATE_TIMESTAMP__lte=timezone.now()
        )

class VerifiedOrgIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    busId = indexes.CharField(model_attr="busId")
    LegalName = indexes.CharField(model_attr="LegalName")

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

class VOClaimTypeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    theType = indexes.CharField(model_attr="busId")

    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.theType,
        ))

    def get_model(self):
        return VOClaimType

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            CREATE_TIMESTAMP__lte=timezone.now()
        )

class VODoingBusinessAsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    DBA = indexes.CharField(model_attr="DBA")

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

class VOLocationTypeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    theType = indexes.CharField(model_attr="theType")
    description = indexes.CharField(model_attr="description")

    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.theType,
            obj.description,
        ))

    def get_model(self):
        return VOLocationType

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            CREATE_TIMESTAMP__lte=timezone.now()
        )

class VOTypeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    theType = indexes.CharField(model_attr="theType")
    description = indexes.CharField(model_attr="description")

    autocomplete = indexes.EdgeNgramField()

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.theType,
            obj.description,
        ))

    def get_model(self):
        return VOType

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            CREATE_TIMESTAMP__lte=timezone.now()
        )