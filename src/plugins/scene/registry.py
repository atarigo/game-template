from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from src.core.events import EventManager

    from .base import GameObject


logger = structlog.get_logger(__name__)


class Registry:
    def __init__(self) -> None:
        self._mappings: dict[str, type["GameObject"]] = {}

    def register(self, name: str, obj_class: type["GameObject"]) -> None:
        if name in self._mappings:
            raise KeyError(f"{name} already registered")

        self._mappings[name] = obj_class

    def create(self, name: str, events: "EventManager") -> "GameObject":
        if name not in self._mappings:
            raise KeyError(f"{name} not registered")

        obj_class = self._mappings[name]
        return obj_class(events=events)
