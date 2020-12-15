import logging

from haystack import indexes

from api.v2.models.Topic import Topic as TopicModel
from api.v2.search.index import TxnAwareSearchIndex

LOGGER = logging.getLogger(__name__)


class TopicIndex(TxnAwareSearchIndex, indexes.Indexable):
    document = indexes.CharField(document=True)

    topic_source_id = indexes.CharField(model_attr="source_id")
    topic_issuer_id = indexes.IntegerField()
    topic_type_id = indexes.IntegerField()
    topic_inactive = indexes.BooleanField()
    topic_revoked = indexes.BooleanField()
    topic_name = indexes.MultiValueField()
    topic_address = indexes.MultiValueField()
    topic_category = indexes.MultiValueField()
    topic_all_credentials_inactive = indexes.BooleanField()
    topic_all_credentials_revoked = indexes.BooleanField()

    def get_model(self):
        return TopicModel

    @staticmethod
    def prepare_topic_issuer_id(obj):
        return obj.foundational_credential.credential_type.issuer_id

    @staticmethod
    def prepare_topic_type_id(obj):
        return obj.foundational_credential.credential_type_id

    @staticmethod
    def prepare_topic_invactive(obj):
        return obj.foundational_credential.inactive

    @staticmethod
    def prepare_topic_revoked(obj):
        return obj.foundational_credential.revoked

    @staticmethod
    def prepare_topic_category(obj):
        return [
            f"{cat.type}::{cat.value}" for cat in obj.foundational_credential.all_categories
        ]

    @staticmethod
    def prepare_topic_name(obj):
        # May need to expand this to inactive credentials
        return [
            name.text for name in obj.get_active_names()
        ]

    @staticmethod
    def prepare_topic_address(obj):
        # May need to expand this to inactive credentials
        return [
            address.civic_address for address in obj.get_active_addresses()
        ]

    @staticmethod
    def prepare_topic_all_credentials_inactive(obj):
        all_creds_inactive = True
        for credential in obj.credentials.all():
            if not credential.inactive:
                all_creds_inactive = False
        return all_creds_inactive

    @staticmethod
    def prepare_topic_all_credentials_revoked(obj):
        all_creds_revoked = True
        for credential in obj.credentials.all():
            if not credential.revoked:
                all_creds_revoked = False
        return all_creds_revoked

    def get_updated_field(self):
        return "update_timestamp"
