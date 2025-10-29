from typing import Type

import pygame

from src.state import SceneState

from .events import EventManager


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


class SceneManager:
    def __init__(self, events: EventManager):
        self.events = events

        self.current: Scene | None = None
        self._scenes: dict[str, Type[Scene]] = {}

        events.subscribe(SceneState.SwitchTo, self.switch_to)

    def register(self, name: str, scene: Type[Scene]):
        self._scenes[name] = scene

    def switch_to(self, data: dict):
        scene_name = data.get("scene_name")
        if next_scene := self._scenes.get(scene_name, None):
            if self.current:
                self.current.on_exit()

            self.current = next_scene(self.events)
            self.current.on_enter()

    def handle_event(self, keydown: pygame.event.Event):
        self.current.handle_event(keydown=keydown)

    def update(self, dt: float):
        self.current.update(dt)

    def draw(self, screen: pygame.Surface):
        self.current.draw(screen)
