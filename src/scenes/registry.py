from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from src.core.events import EventManager
    from src.scenes.base import Scene

logger = structlog.get_logger(__name__)


class SceneRegistry:
    """Factory for creating scene instances"""

    def __init__(self, events: "EventManager"):
        self.events = events
        self.scenes: dict[str, type["Scene"]] = {}

    def register(self, name: str, scene_class: type["Scene"]):
        """Register a scene class with a name"""
        if name in self.scenes:
            logger.warning("Scene already registered, overwriting", scene_name=name)

        self.scenes[name] = scene_class
        logger.info(
            "Scene registered", scene_name=name, scene_class=scene_class.__name__
        )

    def create(self, name: str) -> "Scene":
        """Create a scene instance by name"""
        if name not in self.scenes:
            raise ValueError(f"Scene '{name}' not registered")

        scene_class = self.scenes[name]
        scene_instance = scene_class(self.events)
        logger.debug("Scene instance created", scene_name=name)

        return scene_instance

    def has_scene(self, name: str) -> bool:
        """Check if a scene is registered"""
        return name in self.scenes

    def list_scenes(self) -> list[str]:
        """List all registered scene names"""
        return list(self.scenes.keys())
