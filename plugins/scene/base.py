import pygame
import structlog

from ..core import GameObject
from ..event import EventManager

logger = structlog.get_logger(__name__)


class SceneBase(GameObject):
    def __init__(self, events: EventManager):
        super().__init__()

        self.events = events

    def onkeydown(self, keydown: pygame.event.Event):
        pass

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self.onkeydown(event)


class UIBase(GameObject):
    def __init__(self, events: EventManager):
        super().__init__()

        self.events = events

    def onkeydown(self, keydown: pygame.event.Event):
        pass

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self.onkeydown(event)

    def __hash__(self):
        return hash(self.__class__.__name__)

    def __eq__(self, other):
        return (
            isinstance(other, UIBase)
            and self.__class__.__name__ == other.__class__.__name__
        )
