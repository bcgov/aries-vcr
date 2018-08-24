from django.db import models

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from auditable.models import Auditable

# from .Credential import Credential
# from .TopicRelationship import TopicRelationship

import logging

logger = logging.getLogger(__name__)


class Topic(Auditable):
    source_id = models.TextField()
    type = models.TextField()
    related_topics = models.ManyToManyField(
        "self",
        related_name="+",
        through="TopicRelationship",
        through_fields=("topic", "related_topic"),
        symmetrical=False,
    )

    def save(self, *args, **kwargs):
        """
        Call full_clean to apply form validation on save.
        We use this to prevent insertingtext fields with empty strings.
        """
        self.full_clean()
        super(Topic, self).save(*args, **kwargs)

    class Meta:
        db_table = "topic"
        unique_together = (("source_id", "type"),)
