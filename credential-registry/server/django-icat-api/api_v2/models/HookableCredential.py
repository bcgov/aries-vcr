from django.contrib.postgres import fields as contrib
from django.db import models

from .Auditable import Auditable


class HookableCredential(Auditable):
    # corp_num = models.ForeignKey("Topic", related_name="+", to_field="source_id", on_delete=models.DO_NOTHING)
    # credential_type = models.ForeignKey("CredentialType", related_name="+", on_delete=models.DO_NOTHING)
    corp_num = models.TextField(null=True)
    credential_type = models.TextField(null=True)
    credential_json = contrib.JSONField(blank=True, null=True)

    class Meta:
        db_table = "hookable_cred"
        unique_together = (("corp_num", "credential_type"),)
        ordering = ("corp_num", "credential_type")
