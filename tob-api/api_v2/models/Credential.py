from django.db import models
from django.utils import timezone

from auditable.models import Auditable

from .CredentialType import CredentialType
from .Subject import Subject


class Credential(Auditable):
    subject = models.ForeignKey(Subject, related_name="credentials")
    credential_type = models.ForeignKey(
        CredentialType, related_name="credentials"
    )

    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
