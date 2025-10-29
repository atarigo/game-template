from collections import deque
from typing import Any, Callable

import orjson
import structlog

from .exceptions import exception_handler

logger = structlog.get_logger(__name__)


class EventManager:
    def __init__(self):
        self.listeners: dict[str, list[Callable]] = {}
        self.queue: deque = deque()

    def subscribe(self, event_type: str, callback: Callable):
        logger.info(
            "Subscribing to event",
            event_type=str(event_type),
            callback=callback.__qualname__,
        )

        self.listeners.setdefault(event_type, []).append(callback)

    @exception_handler(ValueError)
    def unsubscribe(self, event_type: str, callback: Callable):
        logger.info(
            "Unsubscribing from event",
            event_type=str(event_type),
            callback=callback.__qualname__,
        )

        if event_type in self.listeners:
            self.listeners[event_type].remove(callback)
            if not self.listeners[event_type]:
                del self.listeners[event_type]

    def emit(self, event_type: str, data: Any = None):
        logger.debug(
            "Emitting event",
            event_type=str(event_type),
            data=orjson.dumps(data).decode("utf-8"),
        )

        self.queue.append((event_type, data))

    @exception_handler(Exception)
    def process_events(self):
        while self.queue:
            event_type, data = self.queue.popleft()
            logger.debug(
                "Processing event",
                event_type=str(event_type),
                data=orjson.dumps(data).decode("utf-8"),
            )

            if event_type in self.listeners:
                for callback in self.listeners[event_type]:
                    callback(data)

    def clear(self):
        if self.queue:
            logger.warning("Event queue is not empty", queue=self.queue)
        self.queue.clear()
