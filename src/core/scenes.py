from typing import TYPE_CHECKING

import pygame

from src.state import SceneStateManager

if TYPE_CHECKING:
    from src.core.events import EventManager
    from src.scenes.base import Scene


class SceneManager:
    def __init__(self, events: "EventManager"):
        self.state = SceneStateManager(events=events)

    @property
    def current(self) -> "Scene":
        return self.state.current

    def register(self, name: str, scene: type["Scene"]):
        self.state.add_scene(name, scene)

    def handle_event(self, keydown: pygame.event.Event):
        self.current.handle_event(keydown=keydown)

    def update(self, dt: float):
        self.current.update(dt)

    def draw(self, screen: pygame.Surface):
        self.current.draw(screen)
