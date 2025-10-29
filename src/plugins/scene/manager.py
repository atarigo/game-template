from typing import TYPE_CHECKING

import pygame
import structlog

from src.core.logs import called

from .events import SceneEvent
from .lifecycle import SceneLifecycle
from .registry import SceneRegistry
from .stack import SceneStack

if TYPE_CHECKING:
    from src.core.events import EventManager

    from .base import Scene

logger = structlog.get_logger(__name__)


class SceneManager:
    """Facade for scene system - coordinates registry, stack, and lifecycle"""

    def __init__(self, events: "EventManager"):
        self.events = events
        self.registry = SceneRegistry(events)
        self.stack = SceneStack()
        self.lifecycle = SceneLifecycle()

        # Subscribe to scene transition events
        events.subscribe(SceneEvent.SWITCH_TO, self._on_switch_to)
        events.subscribe(SceneEvent.PUSH, self._on_push)
        events.subscribe(SceneEvent.POP, self._on_pop)

    @property
    def current(self) -> "Scene | None":
        """Get the current active scene"""
        return self.stack.peek()

    def register(self, name: str, scene_class: type["Scene"]):
        """Register a scene class"""
        self.registry.register(name, scene_class)

    @called
    def _on_switch_to(self, data: dict):
        """Handle SWITCH_TO event - replace entire stack with new scene"""
        scene_name = data.get("scene")
        if not scene_name:
            logger.error("SWITCH_TO event missing 'scene' parameter", data=data)
            return

        try:
            new_scene = self.registry.create(scene_name)
            old_scene = self.stack.peek()

            self.lifecycle.switch(old_scene, new_scene)
            self.stack.clear()
            self.stack.push(new_scene)

            logger.info("Scene switched", scene=scene_name)
        except ValueError as e:
            logger.error("Failed to switch scene", error=str(e), scene=scene_name)

    @called
    def _on_push(self, data: dict):
        """Handle PUSH event - push new scene onto stack"""
        scene_name = data.get("scene")
        if not scene_name:
            logger.error("PUSH event missing 'scene' parameter", data=data)
            return

        try:
            new_scene = self.registry.create(scene_name)
            current_scene = self.stack.peek()

            self.lifecycle.push(current_scene, new_scene)
            self.stack.push(new_scene)

            logger.info("Scene pushed", scene=scene_name)
        except ValueError as e:
            logger.error("Failed to push scene", error=str(e), scene=scene_name)

    @called
    def _on_pop(self, data: dict | None):
        """Handle POP event - pop current scene from stack"""
        if self.stack.is_empty():
            logger.warning("Cannot pop from empty scene stack")
            return

        exiting_scene = self.stack.pop()
        previous_scene = self.stack.peek()

        if exiting_scene:
            self.lifecycle.pop(exiting_scene, previous_scene)
            logger.info("Scene popped", scene=exiting_scene.__class__.__name__)

    def handle_event(self, keydown: pygame.event.Event):
        """Forward event to current scene"""
        if scene := self.current:
            scene.handle_event(keydown=keydown)

    def update(self, dt: float):
        """Forward update to current scene"""
        if scene := self.current:
            scene.update(dt)

    def draw(self, screen: pygame.Surface):
        """Forward draw to current scene"""
        if scene := self.current:
            scene.draw(screen)
