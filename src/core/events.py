from collections import deque
from typing import Any, Callable

import structlog

from .exceptions import exception_handler

logger = structlog.get_logger(__name__)


class EventManager:
    def __init__(self):
        self.listeners: dict[str, list[Callable]] = {}
        self.queue: deque = deque()

    def subscribe(self, event_type: str, callback: Callable):
        self.listeners.setdefault(event_type, []).append(callback)

    @exception_handler(ValueError)
    def unsubscribe(self, event_type: str, callback: Callable):
        if event_type in self.listeners:
            self.listeners[event_type].remove(callback)
            if not self.listeners[event_type]:
                del self.listeners[event_type]

    def emit(self, event_type: str, data: Any = None):
        self.queue.append((event_type, data))

    @exception_handler(Exception)
    def process_events(self):
        while self.queue:
            event_type, data = self.queue.popleft()
            if event_type in self.listeners:
                for callback in self.listeners[event_type]:
                    callback(data)

    def clear(self):
        self.queue.clear()
