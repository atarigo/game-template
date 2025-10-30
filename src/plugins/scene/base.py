import pygame
import structlog

from src.core.events import EventManager

logger = structlog.get_logger(__name__)


class GameObject:
    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self, dt: float):
        pass

    def draw(self, screen: pygame.Surface):
        pass


class SceneBase(GameObject):
    def __init__(self, events: EventManager):
        super().__init__()

        self.events = events

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def onkeydown(self, keydown: pygame.event.Event):
        pass

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self.onkeydown(event)
