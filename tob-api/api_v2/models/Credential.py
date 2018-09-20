from django.db import models
from django.utils import timezone

from auditable.models import Auditable


class Credential(Auditable):
    topic = models.ForeignKey("Topic", related_name="credentials")

    credential_type = models.ForeignKey("CredentialType", related_name="credentials")
    wallet_id = models.TextField(db_index=True)
    credential_def_id = models.TextField(db_index=True, null=True)
    cardinality_hash = models.TextField(db_index=True, null=True)

    effective_date = models.DateTimeField(default=timezone.now)
    inactive = models.BooleanField(db_index=True, default=False)
    revoked = models.BooleanField(db_index=True, default=False)

    class Meta:
        db_table = "credential"
