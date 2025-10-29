from enum import Enum
from typing import TYPE_CHECKING

from src.core.logs import called

if TYPE_CHECKING:
    from src.core.events import EventManager
    from src.scenes.base import Scene


class SceneState(Enum):
    SwitchTo = "SwitchTo"


class SceneStateManager:
    def __init__(self, events: "EventManager"):
        self.events = events

        self.current: "Scene" | None = None
        self.scenes: dict[str, type["Scene"]] = {}

        events.subscribe(SceneState.SwitchTo, self.switch_to)

    def add_scene(self, name: str, scene: type["Scene"]):
        self.scenes[name] = scene

    @called
    def switch_to(self, data: dict):
        scene_name = data.get("scene_name")
        if next_scene := self.scenes.get(scene_name, None):
            if self.current:
                self.current.on_exit()

            self.current = next_scene(self.events)  # new scene instance
            self.current.on_enter()
