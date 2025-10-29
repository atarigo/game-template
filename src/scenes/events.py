from enum import Enum


class SceneEvent(str, Enum):
    """Scene transition event types"""

    SWITCH_TO = "scene.switch_to"
    PUSH = "scene.push"
    POP = "scene.pop"
