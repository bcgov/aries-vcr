from datetime import datetime
import logging
from queue import Empty, Full, Queue
import threading

from api_v2.search.index import TxnAwareSearchIndex
from api_v2.suggest import SuggestManager

LOGGER = logging.getLogger(__name__)


class SolrQueue:
    def __init__(self):
        self._rebuild_count = None
        self._rebuild_time = None
        self._queue = Queue()
        self._stop = threading.Event()
        self._thread = None
        self._trigger = threading.Event()

    def add(self, index_cls, using, ids):
        LOGGER.debug("Solr queue add %s", ids)
        try:
            self._queue.put( (index_cls, using, ids) )
        except Full:
            LOGGER.warning("Solr queue full")

    def setup(self, app):
        app["solrqueue"] = self
        app.on_startup.append(self.app_start)
        app.on_cleanup.append(self.app_stop)

        TxnAwareSearchIndex._backend_queue = self

    async def app_start(self, _app=None):
        self.start()

    async def app_stop(self, _app=None):
        self.stop()

    def start(self):
        self._rebuild_count = 0
        self._rebuild_time = datetime.now()
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def stop(self):
        self._stop.set()
        self._trigger.set()
        self._thread.join()

    def trigger(self):
        self._trigger.set()

    def _run(self):
        while True:
            self._trigger.wait(5)
            if self._stop.is_set():
                return
            self._drain()

    def _drain(self):
        last_index = None
        last_using = None
        last_ids = set()
        while True:
            try:
                index_cls, using, ids = self._queue.get_nowait()
            except Empty:
                index_cls = None
            if last_index and last_index == index_cls and last_using == using:
                last_ids.update(ids)
            else:
                if last_index:
                    self.update(last_index, last_using, last_ids)
                if not index_cls:
                    break
                last_index = index_cls
                last_using = using
                last_ids = set(ids)
        if self._rebuild_count > 1000 or (datetime.now() - self._rebuild_time).seconds > 300:
            self._rebuild_count = 0
            self._rebuild_time = datetime.now()
            SuggestManager().rebuild()

    def update(self, index_cls, using, ids):
        index = index_cls()
        backend = index.get_backend(using)
        if backend is not None:
            LOGGER.debug("Updating %d row(s) in solr queue: %s", len(ids), ids)
            rows = index.index_queryset(using).filter(id__in=ids)
            backend.update(index, rows)
            self._rebuild_count += len(ids)
