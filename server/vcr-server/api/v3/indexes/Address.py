import logging

from haystack import indexes

from api.v2.models.Address import Address as AddressModel
from api.v2.search.index import TxnAwareSearchIndex

LOGGER = logging.getLogger(__name__)


class AddressIndex(TxnAwareSearchIndex, indexes.Indexable):
    document = indexes.CharField(document=True)

    address_addressee = indexes.CharField(model_attr="addressee", null=True)
    address_civic_address = indexes.CharField(model_attr="civic_address", null=True)
    address_city = indexes.CharField(model_attr="city", null=True)
    address_province = indexes.CharField(model_attr="province", null=True)
    address_postal_code = indexes.CharField(model_attr="postal_code", null=True)
    address_country = indexes.CharField(model_attr="country", null=True)

    def get_model(self):
        return AddressModel
