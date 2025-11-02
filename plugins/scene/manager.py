from typing import TYPE_CHECKING

import pygame
import structlog

from .events import SceneEvent, SceneEventData, UIEvent, UIEventData
from .registry import Registry

if TYPE_CHECKING:
    from ..core import GameObject
    from ..event import EventManager


logger = structlog.get_logger(__name__)


class Manager:
    def __init__(self, events: "EventManager"):
        self.events = events
        self.registry = Registry()
        self.children: list["GameObject"] = list()

    def register(self, name: str, obj_class: type["GameObject"]):
        self.registry.register(name, obj_class)

    def handle_event(self, event: pygame.event.Event):
        for child in self.children:
            child.handle_event(event)

    def update(self, dt: float):
        for child in self.children:
            child.update(dt)

    def draw(self, screen: pygame.Surface):
        for child in self.children:
            child.draw(screen)


class UIManager(Manager):
    def __init__(self, events: "EventManager"):
        super().__init__(events=events)

        self.events.subscribe(UIEvent.Toggle, self._toggle)
        self.events.subscribe(UIEvent.Pop, self._pop)

    def _toggle(self, data: UIEventData):
        new_ui = self.registry.create(name=data["name"], events=self.events)

        if new_ui in self.children:
            self.children.remove(new_ui)
        else:
            self.children.append(new_ui)

    def _pop(self, data: UIEventData):
        if self.children:
            self.children.pop()


class SceneManager(Manager):
    def __init__(self, events: "EventManager"):
        super().__init__(events=events)

        self.events.subscribe(SceneEvent.SwitchTo, self._switch_to)
        self.events.subscribe(SceneEvent.Append, self._append)
        self.events.subscribe(SceneEvent.Pop, self._pop)

    def _switch_to(self, data: SceneEventData):
        next_scene = self.registry.create(data["name"], self.events)
        self.children.clear()
        self.children.append(next_scene)

    def _append(self, data: SceneEventData):
        overlay_scene = self.registry.create(data["name"], self.events)
        for child in self.children:
            child.pause = True
        self.children.append(overlay_scene)

    def _pop(self, data: SceneEventData):
        if self.children:
            self.children.pop()
        self.children[-1].pause = False
