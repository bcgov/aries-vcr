from typing import Sequence

from django.contrib.postgres import fields as contrib
from django.db import models

from .Auditable import Auditable
from .Issuer import Issuer
from .Schema import Schema


def _resolve_field_mapping(mapping: dict, name: str):
    field_map = mapping.get(name, {})
    return field_map.get("from") == "claim" and field_map.get("input")


class CredentialType(Auditable):
    schema = models.ForeignKey(
        Schema, related_name="credential_types", on_delete=models.CASCADE
    )
    issuer = models.ForeignKey(
        Issuer, related_name="credential_types", on_delete=models.CASCADE
    )
    description = models.TextField(blank=True, null=True)
    processor_config = contrib.JSONField(blank=True, null=True)
    credential_def_id = models.TextField(db_index=True, null=True)
    logo_b64 = models.TextField(null=True)
    visible_fields = models.TextField(null=True)
    last_issue_date = models.DateTimeField(null=True)
    url = models.TextField(blank=True, null=True)
    credential_title = models.TextField(null=True)
    highlighted_attributes = contrib.JSONField(blank=True, null=True)
    claim_descriptions = contrib.JSONField(blank=True, null=True)
    claim_labels = contrib.JSONField(blank=True, null=True)
    category_labels = contrib.JSONField(blank=True, null=True)

    class Meta:
        db_table = "credential_type"
        unique_together = (("schema", "issuer"),)
        ordering = ("id",)

    def get_has_logo(self):
        return bool(self.logo_b64 or (self.issuer and self.issuer.logo_b64))

    def get_tagged_attributes(self) -> Sequence[str]:
        pconfig = self.processor_config or {}
        fields = set()
        cred_map = pconfig.get("credential", {})
        effective_f = _resolve_field_mapping(cred_map, "effective_date")
        if effective_f:
            fields.add(effective_f)
        topic_defs = pconfig.get("topic", [])
        for topic_def in topic_defs:
            source_id = _resolve_field_mapping(topic_def, "source_id")
            if source_id:
                fields.add(source_id)
        cardinal = pconfig.get("cardinality_fields")
        if cardinal:
            fields.update(cardinal)
        return list(fields)
