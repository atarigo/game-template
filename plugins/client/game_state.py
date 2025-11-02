from enum import Enum
from typing import TYPE_CHECKING

from ..core.logs import called

if TYPE_CHECKING:
    from ..event import EventManager


class GameEvent(Enum):
    Running = "Running"
    Paused = "Paused"
    Unpaused = "Unpaused"
    Quitting = "Quitting"


class GameState(Enum):
    Running = "Running"
    Paused = "Paused"
    Quitting = "Quitting"


class GameStateManager:
    def __init__(self, events: "EventManager"):
        self.current: GameState = GameState.Running

        events.subscribe(GameEvent.Quitting, self._quit_handler)
        events.subscribe(GameEvent.Paused, self._pause_handler)
        events.subscribe(GameEvent.Unpaused, self._unpause_handler)

    @called
    def _pause_handler(self, *args, **kwargs):
        if self.current == GameState.Running:
            self.current = GameState.Paused

    @called
    def _unpause_handler(self, *args, **kwargs):
        if self.current == GameState.Paused:
            self.current = GameState.Running

    @called
    def _quit_handler(self, *args, **kwargs):
        self.current = GameState.Quitting
