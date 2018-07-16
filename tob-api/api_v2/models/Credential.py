from django.db import models
from django.utils import timezone

from auditable.models import Auditable

from .CredentialType import CredentialType
# from .Topic import Topic


class Credential(Auditable):
    topics = models.ManyToManyField('Topic', related_name="credentials")
    credential_type = models.ForeignKey(
        CredentialType, related_name="credentials"
    )
    wallet_id = models.TextField()

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "credential"
