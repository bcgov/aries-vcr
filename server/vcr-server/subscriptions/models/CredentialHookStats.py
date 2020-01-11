from django.contrib.postgres import fields as contrib
from django.db import models

from api.v2.models.Auditable import Auditable


class CredentialHookStats(Auditable):
    """
    Webhook-related statistics
    """

    worker_id = models.TextField(primary_key=True, max_length=64)
    total_count = models.IntegerField(default=0)
    attempt_count = models.IntegerField(default=0)
    success_count = models.IntegerField(default=0)
    fail_count = models.IntegerField(default=0)
    retry_count = models.IntegerField(default=0)
    retry_fail_count = models.IntegerField(default=0)
