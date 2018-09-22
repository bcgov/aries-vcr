from django.db import models

from auditable.models import Auditable


class Attribute(Auditable):
    reindex_related = ["credential"]

    credential = models.ForeignKey("Credential", related_name="attributes", on_delete=models.CASCADE)
    type = models.TextField(db_index=True, default='text')
    format = models.TextField(null=True)
    value = models.TextField(null=True)

    class Meta:
        db_table = "attribute"
        unique_together = (("credential", "type"),)
