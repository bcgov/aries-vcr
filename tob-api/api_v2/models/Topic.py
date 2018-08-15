from django.db import models
from django.db.models import Prefetch

from auditable.models import Auditable

from .Credential import Credential

import logging

logger = logging.getLogger(__name__)


class Topic(Auditable):
    source_id = models.TextField()
    type = models.TextField()

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
                topic_ids.update(
                    list(credential.topics.values_list("id", flat=True))
                )
        # type == incorporation
        else:
            topic_ids = {self.id}

        # Run several smaller queries and process results in application
        # to avoid expensive join
        for credential in credentials:
            c_topic_ids = set(credential.topics.values_list("id", flat=True))
            if c_topic_ids == topic_ids:
                direct_credential_ids.append(credential.id)

        # Give me credentials that have exactly the set of topics `topic_ids``
        # query = (
        #     Credential.objects.annotate(count=models.Count("topics"))
        #     .filter(count=len(topic_ids))
        # )
        # for _id in topic_ids:
        #     query = query.filter(**{"topics": _id})

        # query = query.prefetch_related(
        #     Prefetch(
        #         "topics",
        #         queryset=query,
        #         to_attr="topics",
        #     )
        # )

        return Credential.objects.filter(pk__in=direct_credential_ids)

    class Meta:
        db_table = "topic"
