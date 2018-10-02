import logging

from django.db import transaction
from haystack import indexes

LOGGER = logging.getLogger(__name__)


class TxnAwareSearchIndex(indexes.SearchIndex):
    _backend_queue = None

    def __init__(self, *args, **kwargs):
        super(TxnAwareSearchIndex, self).__init__(*args, **kwargs)
        self._transaction_queued = {}
        self._transaction_savepts = None

    def update_object(self, instance, using=None, **kwargs):
        conn = transaction.get_connection()
        if conn.in_atomic_block:
            if self._transaction_savepts != conn.savepoint_ids:
                self._transaction_savepts = conn.savepoint_ids
                conn.on_commit(self.transaction_committed)
            if self.should_update(instance, **kwargs):
                if not using:
                    using = "default"
                if using not in self._transaction_queued:
                    self._transaction_queued[using] = {}
                self._transaction_queued[using][instance.id] = instance
        else:
            if self._transaction_queued:
                # previous transaction must have ended with rollback
                self._transaction_queued = {}
                self._transaction_savepts = None
            if self._backend_queue:
                self._backend_queue.add(self.__class__, using, [instance.id])
            else:
                super(TxnAwareSearchIndex, self).update_object(instance, using, **kwargs)

    def transaction_committed(self):
        conn = transaction.get_connection()
        if conn.in_atomic_block:
            # committed nested transaction - ensure hook is attached
            self._transaction_savepts = conn.savepoint_ids
            conn.on_commit(self.transaction_committed)
        else:
            for using, instances in self._transaction_queued.items():
                if instances:
                    LOGGER.debug("Committing %d deferred Solr update(s) after transaction", len(instances))
                    if self._backend_queue:
                        self._backend_queue.add(self.__class__, using, list(instances.keys()))
                    else:
                        backend = self.get_backend(using)
                        if backend is not None:
                            backend.update(self, instances.values())
            self._transaction_queued = {}
            self._transaction_savepts = None
