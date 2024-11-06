from dataclasses import dataclass
import logging
import queue
import atexit
from datetime import datetime, timezone
import time
from uuid import uuid4
import json
from openanalytics.consumer import Consumer, MAX_MSG_SIZE
from openanalytics.request import DatetimeSerializer
from openanalytics.utils import *
from openanalytics.connectors import ConnectorInterface
from openanalytics.models import Identify, Track, Page, Token, Log


@dataclass
class OpenAnalytics:
    """Create a new open-analytics client."""

    host: str = "http://localhost"
    on_error = None
    debug: bool = False
    log_handler = None
    send: bool = True
    sync_mode: bool = False
    max_queue_size: int = 10000
    thread: int = 1
    connector: ConnectorInterface = None

    _model_types = [
        Identify.__name__,
        Track.__name__,
        Page.__name__,
        Token.__name__,
        Log.__name__,
    ]

    # queues: list[dict:{queue, str}] = []
    queue = queue.Queue(max_queue_size)

    log = logging.getLogger("open-analytics")

    if log_handler:
        log.addHandler(log_handler)

    if debug:
        log.setLevel(logging.DEBUG)
        if not log_handler:
            # default log handler does not print debug or info
            log.addHandler(logging.StreamHandler())

    def __init__(
        self,
        connector: ConnectorInterface,
        sync_mode: bool = False,
        max_threads=1,
        debug=False,
        log_handler=None,
        send=True,
    ):

        self.connector = connector
        self.sync_mode = sync_mode
        self.thread = max_threads
        self.debug = debug
        self.log_handler = log_handler
        self.send = send

        if self.log_handler:
            self.log.addHandler(self.log_handler)

        if self.debug:
            self.log.setLevel(logging.DEBUG)
            if not self.log_handler:
                # default log handler does not print debug or info
                self.log.addHandler(logging.StreamHandler())

        if sync_mode:
            self.consumers = None
        else:
            # On program exit, allow the consumer thread to exit cleanly.
            # This prevents exceptions and a messy shutdown when the
            # interpreter is destroyed before the daemon thread finishes
            # execution. However, it is *not* the same as flushing the queue!
            # To guarantee all messages have been delivered, you'll still need
            # to call flush().
            if self.send:
                atexit.register(self.join)

            self.consumers = []
            for _ in range(self.thread):
                consumer = Consumer(self.queue, self.connector)
                self.consumers.append(consumer)

                # if we've disabled sending, just don't start the consumer
                if self.send:
                    consumer.start()

    def identify(self, data: Identify) -> tuple:
        """The Identify method lets you tie a user to their actions and record traits about them. It includes a unique User ID and any optional traits you know about them."""

        data.type = Identify.SIGNATURE
        require("userId", data.userId, str)
        require("event", data.event, str)
        msg = data.__dict__
        return self._push_to_queue(msg)

    def track(self, data: Track) -> tuple:
        """Track lets you record the actions your users perform. Every action triggers what Segment calls an “event”, which can also have associated properties."""

        data.type = Track.SIGNATURE
        require("endpoint", data.endpoint, str)
        require("event", data.event, str)
        require("properties", data.properties, dict)
        msg = data.__dict__
        return self._push_to_queue(msg)

    def page(self, data: Page) -> tuple:
        """The Page method lets you record page views on your website, along with optional extra information about the page being viewed."""

        data.type = Page.SIGNATURE
        require("name", data.name, str)
        require("category", data.category, str)
        require("properties", data.properties, dict)
        msg = data.__dict__
        return self._push_to_queue(msg)

    def token(self, data: Token) -> tuple:
        """The Token method lets you record token utlization for you events, along with optional extra information about the token processing."""

        data.type = Token.SIGNATURE
        require("event", data.event, str)
        require("action", data.action, str)
        require("count", data.count, int)
        msg = data.__dict__
        return self._push_to_queue(msg)

    def logger(self, data: Log) -> tuple:
        """The Log method lets you record log events of your actions, along with optional extra information about the log event."""

        data.type = Log.SIGNATURE
        require("summary", data.summary, str)
        require("level", data.level, str)
        require("event", data.event, str)
        msg = data.__dict__
        return self._push_to_queue(msg)

    def _push_to_queue(self, msg) -> tuple:
        """Push a new `msg` onto the queue, return `(success, msg)`"""

        timestamp = msg["timestamp"]
        if timestamp is None:
            msg["timestamp"] = datetime.now(timezone.utc)

        _time = msg["time"]
        if _time is None:
            msg["time"] = time.time()

        message_id = msg.get("messageId")
        if message_id is None:
            message_id = uuid4()
            msg["messageId"] = stringify_id(message_id)

        require("type", msg["type"], str)
        require("timestamp", msg["timestamp"], datetime)
        require("messageId", msg["messageId"], str)

        msg_size = len(json.dumps(msg, cls=DatetimeSerializer).encode())
        if msg_size > MAX_MSG_SIZE:
            raise RuntimeError(
                "Message exceeds %skb limit. (%s)",
                str(int(MAX_MSG_SIZE / 1024)),
                str(msg),
            )

        if not self.send:
            return (True, msg)

        if self.sync_mode:
            self.log.debug("enqueued with blocking %s.", msg["type"])
            self.connector.load(msg["type"], msg)

            return (True, msg)

        try:
            _type = msg["type"]
            self.queue.put((_type, msg), block=False)
            self.log.debug(f"enqueued {_type} - {msg}. \n")
            return (True, msg)
        except queue.Full:
            self.log.warning("open-analytics queue is full")
            return (False, msg)

    def flush(self):
        """Forces a flush from the internal queue to the server"""

        queue = self.queue
        size = queue.qsize()
        self.log.debug("flushing queue with %s items.", size)
        if size > 0:
            queue.join()
        # Note that this message may not be precise, because of threading.
        self.log.debug("successfully flushed about %s items.", size)

    def join(self):
        """Ends the consumer thread once the queue is empty.
        Blocks execution until finished
        """
        _count = len(self.consumers)
        self.log.debug("joining consumers with %s items.", _count)
        if self.consumers is not None:
            for consumer in self.consumers:
                consumer.pause()
                try:
                    consumer.join()
                except RuntimeError:
                    # consumer thread has not started
                    pass

    def shutdown(self):
        """Flush all messages and cleanly shutdown the client"""
        self.log.debug("shutting down client")
        self.flush()
        self.join()
