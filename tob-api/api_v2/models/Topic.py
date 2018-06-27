from django.db import models

from auditable.models import Auditable


class Topic(Auditable):
    source_id = models.TextField()
    type = models.TextField()

    class Meta:
        db_table = "topic"
