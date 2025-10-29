import pygame

from src.core.events import EventManager


class Scene:
    def __init__(self, events: EventManager):
        self.events: EventManager = events

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def handle_event(self, keydown: pygame.event.Event):
        pass

    def update(self, dt: float):
        pass

    def draw(self, screen: pygame.Surface):
        pass
