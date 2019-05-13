from django.db import models
from django.utils import timezone

from .Auditable import Auditable


class Credential(Auditable):
    topic = models.ForeignKey("Topic", related_name="credentials", on_delete=models.CASCADE)
    credential_set = models.ForeignKey("CredentialSet", related_name="credentials", null=True, on_delete=models.CASCADE)
    credential_type = models.ForeignKey("CredentialType", related_name="credentials", on_delete=models.CASCADE)
    wallet_id = models.TextField(db_index=True)
    credential_def_id = models.TextField(db_index=True, null=True)
    cardinality_hash = models.TextField(db_index=True, null=True)

    effective_date = models.DateTimeField(default=timezone.now)
    inactive = models.BooleanField(db_index=True, default=False)
    latest = models.BooleanField(db_index=True, default=False)
    revoked = models.BooleanField(db_index=True, default=False)
    revoked_date = models.DateTimeField(null=True)
    revoked_by = models.ForeignKey("Credential", related_name="+", null=True, on_delete=models.SET_NULL)

    # Topics related by this credential
    related_topics = models.ManyToManyField(
        "Topic",
        # Topics that have a verifiable relationship to me
        related_name="related_via",
        through="TopicRelationship",
        through_fields=("credential", "related_topic"),
        symmetrical=False,
    )

    class Meta:
        db_table = "credential"
        ordering = ('id',)

    _cache = None
    def _cached(self, key, val):
        cache = self._cache
        if cache is None:
            self._cache = cache = {}
        if key not in cache:
            cache[key] = val
        return cache[key]

    # used by solr document index
    @property
    def all_names(self):
        return self._cached('names', self.names.all())

    @property
    def all_categories(self):
        return self._cached('categories', self.attributes.filter(format='category'))

    @property
    def all_attributes(self):
        return self._cached('attributes', self.attributes.all())
