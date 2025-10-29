from enum import Enum

from src.core.events import EventManager


class GameState(Enum):
    Running = "GameRunning"
    Quitting = "GameQuitting"


class GameStateManager:
    def __init__(self, events: EventManager):
        self.current: GameState = GameState.Running

        events.subscribe(GameState.Quitting, self.game_quit_handler)

    def game_quit_handler(self, *args, **kwargs):
        self.current = GameState.Quitting
