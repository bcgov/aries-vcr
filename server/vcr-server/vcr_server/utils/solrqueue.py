import logging
import threading
from queue import Empty, Full, Queue

from haystack.utils import get_identifier

from api.v2.search.index import TxnAwareSearchIndex

LOGGER = logging.getLogger(__name__)


class SolrQueue:
    def __init__(self):
        LOGGER.info("Initializing Solr queue ...")
        self._queue = Queue()
        self._prev_queue = None
        self._stop = threading.Event()
        self._thread = None
        self._trigger = threading.Event()

    def add(self, index_cls, using, instances):
        ids = [instance.id for instance in instances]
        # Log the wallet_id to make it easy to search for the credentials when troubleshooting
        # The record ids are not indexed so they are not searchable.
        wallet_ids = [instance.credential_id for instance in instances]
        LOGGER.debug("Adding items to Solr queue for indexing; Class: %s, Using: %s, Instances: %s", index_cls, using, wallet_ids)
        try:
            self._queue.put((index_cls, using, ids, 0))
        except Full:
            LOGGER.warning("Can't add items to the Solr queue because it is full; %s", wallet_ids)

    def delete(self, index_cls, using, instances):
        ids = [get_identifier(instance) for instance in instances]
        # Log the wallet_id to make it easy to search for the credentials when troubleshooting
        # The record ids are not indexed so they are not searchable.
        wallet_ids = [instance.credential_id for instance in instances]
        LOGGER.debug("Deleteing items from Solr queue/index; Class: %s, Using: %s, Instances: %s", index_cls, using, wallet_ids)
        try:
            self._queue.put((index_cls, using, ids, 1))
        except Full:
            LOGGER.warning("Can't delete items from the Solr queue because it is full; %s", wallet_ids)

    def setup(self, app=None):
        LOGGER.info("Setting up Solr queue ...")
        if app is not None:
            LOGGER.info("Wiring the Solr queue into the app; %s", app)
            app["solrqueue"] = self
            app.on_startup.append(self.app_start)
            app.on_cleanup.append(self.app_stop)
        LOGGER.info("Wiring the Solr queue into the TxnAwareSearchIndex.")
        self._prev_queue = TxnAwareSearchIndex._backend_queue
        TxnAwareSearchIndex._backend_queue = self

    async def app_start(self, _app=None):
        self.start()

    async def app_stop(self, _app=None):
        self.stop()

    def __enter__(self):
        self.setup()
        self.start()
        return self

    def __exit__(self, type, value, tb):
        LOGGER.info("Solr queue is exiting ...")
        # if handling exception, don't wait for worker thread
        self.stop(not type)
        LOGGER.info("Restoring previous TxnAwareSearchIndex settings ...")
        TxnAwareSearchIndex._backend_queue = self._prev_queue

    def start(self):
        LOGGER.info("Starting Solr queue ...")
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def stop(self, join=True):
        LOGGER.info("Stoping Solr queue ...")
        if not self._queue.empty():
            LOGGER.warning("The Solr queue is not empty, there are about %s items that will not be indexed", self._queue.qsize())
        self._stop.set()
        self._trigger.set()
        if join:
            self._thread.join()

    def trigger(self):
        LOGGER.info("Triggering Solr queue ...")
        self._trigger.set()

    def _run(self):
        LOGGER.info("Running Solr queue ...")
        while True:
            self._trigger.wait(5)
            self._drain()
            if self._stop.is_set():
                LOGGER.info("Finished running Solr queue ...")
                return

    def _drain(self):
        # LOGGER.debug("Indexing Solr queue items ...")
        last_index = None
        last_using = None
        last_del = 0
        last_ids = set()
        while True:
            try:
                index_cls, using, ids, delete = self._queue.get_nowait()
                LOGGER.debug("Pop items off the Solr queue for indexing; Class: %s, Using: %s, Delete: %s, Instances: %s", index_cls, using, delete, ids)
            except Empty:
                # LOGGER.debug("Solr queue is empty ...")
                index_cls = None
            if last_index and last_index == index_cls and last_using == using and last_del == delete:
                LOGGER.debug("Updating list of ids ...")
                last_ids.update(ids)
            else:
                if last_index:
                    try:
                        if last_del:
                            self.remove(last_index, last_using, last_ids)
                        else:
                            self.update(last_index, last_using, last_ids)
                    except:
                        LOGGER.exception("An unexpected exception was encountered while processing items from the Solr queue.", exc_info=True)
                        LOGGER.info("Requeueing items for later processing ...")
                        try:
                            self._queue.put( (last_index, last_using, last_ids, last_del) )
                        except Full:
                            LOGGER.warning("Can't requeue items to the Solr queue because it is full; %s", last_ids)

                if not index_cls:
                    # LOGGER.debug("Done indexing items from Solr queue ...")
                    break

                last_index = index_cls
                last_using = using
                last_del = delete
                last_ids = set(ids)

    def update(self, index_cls, using, ids):
        LOGGER.debug("Updating the indexes for Solr queue items ...")
        index = index_cls()
        backend = index.get_backend(using)
        if backend is not None:
            LOGGER.info("Updating indexes for %d row(s) from Solr queue: %s", len(ids), ids)
            rows = index.index_queryset(using).filter(id__in=ids)
            # Turn off silently_fail; throw an exception if there is an error so we can requeue the items being indexed.
            backend.silently_fail = False
            backend.update(index, rows)
            # LOGGER.debug("Index update complete.")
        else:
            LOGGER.error("Failed to get backend.  Unable to update the index for %d row(s) from the Solr queue: %s", len(ids), ids)

    def remove(self, index_cls, using, ids):
        LOGGER.debug("Removing the indexes for Solr queue items ...")
        index = index_cls()
        backend = index.get_backend(using)
        if backend is not None:
            LOGGER.info("Removing indexes for %d row(s) in Solr queue: %s", len(ids), ids)
            # Turn off silently_fail; throw an exception if there is an error so we can requeue the items being indexed.
            backend.silently_fail = False
            # backend.remove has no support for a list of IDs
            backend.conn.delete(id=ids)
        else:
            LOGGER.error("Failed to get backend.  Unable to remove the indexes for %d row(s) from the solr queue: %s", len(ids), ids)
