import logging

from haystack import indexes

from api.v2.models.Name import Name as NameModel
from api.v2.search.index import TxnAwareSearchIndex

LOGGER = logging.getLogger(__name__)


class NameIndex(TxnAwareSearchIndex, indexes.Indexable):
    document = indexes.CharField(document=True)

    name_text = indexes.CharField(model_attr="text")
    name_type = indexes.CharField(model_attr="type")
    name_credential_inactive = indexes.BooleanField()
    name_credential_revoked = indexes.BooleanField()

    def get_model(self):
        return NameModel

    @staticmethod
    def prepare_name_credential_inactive(obj):
        return obj.credential.inactive

    @staticmethod
    def prepare_name_credential_revoked(obj):
        return obj.credential.revoked

    def get_updated_field(self):
        return "update_timestamp"
