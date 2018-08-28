from django.db import models
from django.utils import timezone

from auditable.models import Auditable

# from .Credential import Credential
from .Topic import Topic


class TopicRelationship(Auditable):
    credential = models.ForeignKey("Credential", related_name="+")
    topic = models.ForeignKey(Topic, related_name="+")
    related_topic = models.ForeignKey(Topic, related_name="+")

    class Meta:
        db_table = "topic_relationship"
