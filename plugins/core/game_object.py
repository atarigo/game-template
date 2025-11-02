from typing import Protocol

import pygame


class GameObject(Protocol):
    def handle_event(self, event: pygame.event.Event, *args, **kwargs):
        pass

    def update(self, dt: float, *args, **kwargs):
        pass

    def draw(self, screen: pygame.Surface, *args, **kwargs):
        pass
