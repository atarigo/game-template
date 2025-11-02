from enum import Enum
from typing import TYPE_CHECKING

from ..core.logs import called

if TYPE_CHECKING:
    from ..event import EventManager


class GameEvent(Enum):
    Running = "Running"
    Quitting = "Quitting"


class GameStateManager:
    def __init__(self, events: "EventManager"):
        self.current: GameEvent = GameEvent.Running

        events.subscribe(GameEvent.Quitting, self.game_quit_handler)

    @called
    def game_quit_handler(self, *args, **kwargs):
        self.current = GameEvent.Quitting
