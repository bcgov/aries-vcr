from django.db import models
from django.db.models import Prefetch

from auditable.models import Auditable

from .Credential import Credential

import logging

logger = logging.getLogger(__name__)


class Topic(Auditable):
    source_id = models.TextField()
    type = models.TextField()

    def direct_credentials(self):
        """
        Returns credentials that are directly related to
        this topic and not related due a "child" topic
        relation. i.e., an incorporation's credentials
                        and not its DBA's credentials
        """

        # TODO: allow an issuer to register its topic
        #       formation and make this dynamic
        if self.type == "doing_business_as":
            credentials = self.credentials.all()
            topic_ids = set()
            for credential in credentials:
                topic_ids.update(
                    list(credential.topics.values_list("id", flat=True))
                )
        else:
            topic_ids = {self.id}

        query = (
            Credential.objects.annotate(count=models.Count("topics"))
            .filter(count=len(topic_ids))
        )

        for _id in topic_ids:
            query = query.filter(**{"topics": _id})

        query = query.prefetch_related(
            Prefetch(
                "topics",
                queryset=query,
                to_attr="topics",
            )
        )

        return query

    class Meta:
        db_table = "topic"
