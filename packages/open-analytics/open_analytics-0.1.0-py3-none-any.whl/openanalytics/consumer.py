import logging
from threading import Thread
import time
from openanalytics.connectors import ConnectorInterface
from openanalytics.request import DatetimeSerializer
import json
from queue import Empty
from dataclasses import dataclass
from openanalytics.version import APP_NAME


MAX_MSG_SIZE = 32 << 10
BATCH_SIZE_LIMIT = 450 * 1024


@dataclass
class CollectionItem:
    name: str
    items: list


class Consumer(Thread):
    """Consumes the messages from the client's queue."""

    upload_size: int = 100
    upload_interval: float = 10
    log = logging.getLogger(APP_NAME)

    def __init__(self, queue, connector: ConnectorInterface):
        Thread.__init__(self)

        self.connector = connector
        self.queue = queue
        self.running = True

    def run(self):
        """Runs the consumer."""
        self.log.debug("consumer is running...")
        while self.running:
            self.upload()

        self.log.debug("consumer exited.")

    def pause(self):
        """Pause the consumer."""
        self.running = False

    def upload(self):
        """Upload the next batch of items, return whether successful."""
        success = False
        batches = self.next()
        if len(batches) == 0:
            return False

        try:
            for batch in batches:
                self.connector.bulk_load(collection_name=batch.name, msg=batch.items)
            success = True
        except Exception as e:
            self.log.error("error uploading: %s", e)
            success = False
            if self.on_error:
                self.on_error(e, batches)
        finally:
            # mark items as acknowledged from queue
            for _ in batches:
                self.queue.task_done()
            return success

    def next(self):
        """Return the next batch of items to upload."""

        queue = self.queue
        items = []

        start_time = time.monotonic()
        total_size = 0

        while len(items) < self.upload_size:
            elapsed = time.monotonic() - start_time
            if elapsed >= self.upload_interval:
                break
            try:
                item = queue.get(block=True, timeout=self.upload_interval - elapsed)
                item_size = len(json.dumps(item, cls=DatetimeSerializer).encode())
                if item_size > MAX_MSG_SIZE:
                    self.log.error("Item exceeds 32kb limit, dropping. (%s)", str(item))
                    continue
                items.append(item)
                total_size += item_size
                if total_size >= BATCH_SIZE_LIMIT:
                    self.log.debug("hit batch size limit (size: %d)", total_size)
                    break
            except Empty:
                break
            except Exception as e:
                self.log.exception("Exception: %s", e)

        collections: list[CollectionItem] = []

        for item in items:
            specific_collection = next(
                (p for p in collections if p.name == item[0]), None
            )
            if specific_collection is not None:
                index = [p for p in collections].index(specific_collection)
                collections[index].items.append(item[1])
            else:
                collection_item = CollectionItem(name=item[0], items=[item[1]])
                collections.append(collection_item)

        return collections
