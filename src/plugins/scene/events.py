from enum import Enum
from typing import TypedDict


class SceneEvent(Enum):
    SwitchTo = "SwitchTo"
    Append = "Append"
    Pop = "Pop"


class UIEvents(Enum):
    Toggle = "Toggle"
    Pop = "Pop"


class SceneEventData(TypedDict):
    name: str


class UIEventData(TypedDict):
    name: str
