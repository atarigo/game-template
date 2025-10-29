from typing import Type

import pygame

from src.scenes.base import Scene
from src.state import SceneStateManager

from .events import EventManager


class SceneManager:
    def __init__(self, events: EventManager):
        self.state = SceneStateManager(events=events)

    @property
    def current(self) -> Scene | None:
        return self.state.current

    def register(self, name: str, scene: Type[Scene]):
        self.state.add_scene(name, scene)

    def handle_event(self, keydown: pygame.event.Event):
        self.current.handle_event(keydown=keydown)

    def update(self, dt: float):
        self.current.update(dt)

    def draw(self, screen: pygame.Surface):
        self.current.draw(screen)
