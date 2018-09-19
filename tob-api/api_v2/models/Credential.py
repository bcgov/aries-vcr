from django.db import models
from django.utils import timezone

from auditable.models import Auditable

from .Address import Address
from .Category import Category


class Credential(Auditable):
    topic = models.ForeignKey("Topic", related_name="credentials")

    credential_type = models.ForeignKey("CredentialType", related_name="credentials")
    wallet_id = models.TextField(db_index=True)
    credential_def_id = models.TextField(db_index=True, null=True)
    cardinality_hash = models.TextField(db_index=True, null=True)

    effective_date = models.DateTimeField(default=timezone.now)
    revoked = models.BooleanField(db_index=True, default=False)

    _topic_cred_ids = None

    class Meta:
        db_table = "credential"

    def get_topic_active_credential_ids(self):
        if self._topic_cred_ids is None:
            self._topic_cred_ids = set(self.topic.credentials.filter(revoked=False)\
                .only('id', 'topic_id').values_list('id', flat=True))
        return self._topic_cred_ids

    def get_topic_addresses(self):
        creds = self.get_topic_active_credential_ids()
        if creds:
            return Address.objects.filter(credential_id__in=creds)
        return []

    def get_topic_categories(self):
        creds = self.get_topic_active_credential_ids()
        if creds:
            return Category.objects.filter(credential_id__in=creds)
        return []
