import logging
import os
import threading
from queue import Empty, Full, Queue

from api.v2.search.index import TxnAwareSearchIndex
from haystack.utils import get_identifier

LOGGER = logging.getLogger(__name__)


# this will kill the vcr-api process
RTI_ABORT_ON_ERRORS = os.getenv("RTI_ABORT_ON_ERRORS", "TRUE").upper()
ABORT_ON_ERRORS = RTI_ABORT_ON_ERRORS == "TRUE"
# this will re-raise errors, which will kill the indexing thread
RTI_RAISE_ERRORS = os.getenv("RTI_RAISE_ERRORS", "FALSE").upper()
RAISE_ERRORS = RTI_RAISE_ERRORS == "TRUE"
# if both of the above are false, indexing errors will be ignored

# number of seconds to wait when solr queue is empty before retry
RTI_WAIT_TIME = os.getenv("RTI_WAIT_TIME", "5")
WAIT_TIME = int(RTI_WAIT_TIME)

# max number of items to trigger an update to the solr index
RTI_MAX_SOLR_BATCH = os.getenv("RTI_MAX_SOLR_BATCH", "25")
MAX_SOLR_BATCH = int(RTI_MAX_SOLR_BATCH)


class SolrQueue:
    is_active = False

    def __init__(self):
        LOGGER.info("Initializing Solr queue ...")
        self._queue = Queue()
        self._prev_queue = None
        self._stop = threading.Event()
        self._thread = None
        self._trigger = threading.Event()

    def isactive(self):
        return (self.is_active or not self._queue.empty())

    def qsize(self):
        return self._queue.qsize()

    def add(self, index_cls, using, instances):
        ids = [instance.id for instance in instances]
        # Log the wallet_id to make it easy to search for the credentials when troubleshooting
        # The record ids are not indexed so they are not searchable.
        # wallet_ids = [instance.credential_id for instance in instances]
        LOGGER.debug("Adding items to Solr queue for indexing; Class: %s, Using: %s", index_cls, using)
        try:
            self._queue.put((index_cls, using, ids, 0))
        except Full:
            LOGGER.error("Can't add items to the Solr queue because it is full")
            raise

    def delete(self, index_cls, using, instances):
        ids = [get_identifier(instance) for instance in instances]
        # Log the wallet_id to make it easy to search for the credentials when troubleshooting
        # The record ids are not indexed so they are not searchable.
        # wallet_ids = [instance.credential_id for instance in instances]
        LOGGER.debug("Deleteing items from Solr queue/index; Class: %s, Using: %s", index_cls, using)
        try:
            self._queue.put((index_cls, using, ids, 1))
        except Full:
            LOGGER.error("Can't delete items from the Solr queue because it is full")
            raise

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
            LOGGER.error("The Solr queue is not empty, there are about %s items that will not be indexed", self._queue.qsize())
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
            LOGGER.debug("Waiting [%d] ...", WAIT_TIME)
            self._trigger.wait(WAIT_TIME)
            self._drain()
            if self._stop.is_set():
                LOGGER.info("Finished running Solr queue ...")
                return


    def index_type(self, index_cls, delete, using):
        """String representing the index class type."""
        if not index_cls:
            return None
        return ("delete" if delete == 1 else "update") + "::" + str(index_cls) + "::" + str(using)


    def _drain(self):
        LOGGER.debug("Indexing Solr queue items ...")
        global RAISE_ERRORS
        global ABORT_ON_ERRORS
        last_ids = {}
        try:
            self.is_active = True
            while True:
                try:
                    index_cls, using, ids, delete = self._queue.get_nowait()
                    LOGGER.debug("Pop items off the Solr queue for indexing; Class: %s, Using: %s, Delete: %s, Instances: %s", index_cls, using, delete, ids)
                except Empty:
                    LOGGER.debug("Solr queue is empty ...")
                    index_cls = None
                    delete = 0
                    using = None
                index_cls_type = self.index_type(index_cls, delete, using)
                if index_cls:
                    LOGGER.debug("Updating list of ids for [%s]..." % index_cls_type)
                    if not index_cls_type in last_ids:
                        last_ids[index_cls_type] = {
                            "index_cls": index_cls,
                            "delete": delete,
                            "using": using,
                            "ids": set(),
                        }
                    last_ids[index_cls_type]["ids"].update(ids)
                for attr, val in last_ids.items():
                    if (not index_cls) or MAX_SOLR_BATCH <= len(val["ids"]):
                        LOGGER.debug("Processing %s items for [%s]", len(val["ids"]), attr)
                        try:
                            if val["delete"] == 1:
                                self.remove(val["index_cls"], val["using"], val["ids"])
                            else:
                                self.update(val["index_cls"], val["using"], val["ids"])
                            last_ids[attr]["ids"] = set()
                        except:
                            LOGGER.exception("An unexpected exception was encountered while processing items from the Solr queue.", exc_info=True)
                            LOGGER.info("Requeueing items for later processing ...")
                            try:
                                self._queue.put( (val["index_cls"], val["using"], val["ids"], val["delete"]) )
                            except Full:
                                LOGGER.error("Can't requeue items to the Solr queue because it is full; %s", val["ids"])
                                raise
                            raise

                if not index_cls:
                    LOGGER.debug("Done indexing items from Solr queue ...")
                    break

        except Exception as e:
            LOGGER.error("Error processing real-time index queue: %s", str(e))
            if ABORT_ON_ERRORS:
                # this will kill the vcr-api process
                os.abort()
            elif RAISE_ERRORS:
                # this will re-raise errors, which will kill the indexing thread
                raise
            # if both of the above are false, indexing errors will be ignored
        finally:
            self.is_active = False

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
            raise Exception("Failed to get backend.  Unable to update the index for Solr queue")

    def remove(self, index_cls, using, ids):
        LOGGER.debug("Removing the indexes for Solr queue items ...")
        index = index_cls()
        backend = index.get_backend(using)
        if backend is not None:
            LOGGER.info("Removing indexes for %d row(s) in Solr queue: %s", len(ids), ids)
            # Turn off silently_fail; throw an exception if there is an error so we can requeue the items being indexed.
            backend.silently_fail = False
            # backend.remove has no support for a list of IDs
            if len(ids) > 0:
                backend.conn.delete(id=ids)
            else:
                LOGGER.warning("No IDs provided for deletion from Solr queue, skipping.")
        else:
            LOGGER.error("Failed to get backend.  Unable to remove the indexes for %d row(s) from the solr queue: %s", len(ids), ids)
            raise Exception("Failed to get backend.  Unable to remove the index for Solr queue")
