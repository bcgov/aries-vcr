from django.db import models
from django.utils import timezone

from auditable.models import Auditable

from .CredentialType import CredentialType
# from .Topic import Topic


class Credential(Auditable):
    reindex_related = ['topics']

    topics = models.ManyToManyField('Topic', related_name="credentials")
    credential_type = models.ForeignKey(
        CredentialType, related_name="credentials"
    )
    wallet_id = models.TextField()

    effective_date = models.DateTimeField(default=timezone.now)
    revoked = models.BooleanField(default=False)

    class Meta:
        db_table = "credential"
