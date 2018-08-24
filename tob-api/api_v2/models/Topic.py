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

    def direct_credentials(self, filter_args={}):
        """
        Returns credentials that are directly related to
        this topic and not related due a "child" topic
        relation. i.e., an incorporation's credentials
                        and not its DBA's credentials
        """

        # TODO: allow an issuer to register its topic
        #       formation and make this dynamic
        direct_credential_ids = []
        credentials = self.credentials.all()

        if self.type == "doing_business_as":

            topic_ids = set()
            for credential in credentials:
                # distinct
                topic_ids.update(list(credential.topics.values_list("id", flat=True)))
        # type == incorporation
        else:
            topic_ids = {self.id}

        # Run several smaller queries and process results in application
        # to avoid expensive join
        for credential in credentials:
            c_topic_ids = set(credential.topics.values_list("id", flat=True))
            if c_topic_ids == topic_ids:
                direct_credential_ids.append(credential.id)

        return Credential.objects.filter(pk__in=direct_credential_ids)

    class Meta:
        db_table = "topic"
