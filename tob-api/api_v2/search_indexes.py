# TODO: Figure out how to configure haystack to register indices in
#       ./indices/<IndexName> instead of this default file...

from itertools import chain

from haystack import indexes
from django.db.models import Prefetch
from django.utils import timezone

from api_v2.models.Credential import Credential as CredentialModel
from api_v2.models.Name import Name as NameModel
from api_v2.models.Topic import Topic as TopicModel


class TopicIndex(indexes.SearchIndex, indexes.Indexable):
    document = indexes.CharField(document=True, use_template=True)

    name = indexes.MultiValueField()
    location = indexes.MultiValueField()
    # historical = indexes.BooleanField()

    @staticmethod
    def prepare_name(obj):
        names = ((name.text for name in cred.names.all()) for cred in obj.nonrevoked)
        return list(chain.from_iterable(names))

    @staticmethod
    def prepare_location(obj):
        locations = []
        for credential in obj.nonrevoked:
            for address in credential.addresses.all():
                loc = " ".join(filter(None, (
                  address.addressee,
                  address.civic_address,
                  address.city,
                  address.province,
                  address.postal_code,
                  address.country,
                )))
                if loc:
                  locations.append(loc)
        return locations

    def get_model(self):
        return TopicModel

    def index_queryset(self, using=None):
        creds = CredentialModel.objects.filter(revoked=False)
        names = NameModel.objects.all().only('id', 'credential_id', 'text')
        prefetch = (
            Prefetch('credentials', queryset=creds, to_attr='nonrevoked'),
            Prefetch('nonrevoked__names', queryset=names),
            'nonrevoked__addresses',
        )
        return self.get_model().objects.filter(
            create_timestamp__lte=timezone.now()
        ).prefetch_related(*prefetch)
