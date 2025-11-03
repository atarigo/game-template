from typing import TYPE_CHECKING

import pygame
import structlog

from .game_state import GameEvent, GameState, GameStateManager

if TYPE_CHECKING:
    from ..core import Settings
    from ..event import EventManager
    from ..scene import SceneManager


logger = structlog.get_logger(__name__)


class Game:
    def __init__(
        self,
        settings: "Settings",
        events: "EventManager",
        scene_manager: "SceneManager",
    ):
        self.events = events
        self.scene_manager = scene_manager

        self.state = GameStateManager(events=events)

        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

    def run(self):
        while self.state.current == GameState.Running:
            if self.state.current == GameState.Paused:
                # for game saving, we need to pause the game
                continue

            dt = self.clock.tick(60) / 1000  # seconds

            self.handle_events()
            self.update(dt)
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.events.emit(GameEvent.Quitting)

            self.scene_manager.handle_event(event=event)

    def update(self, dt: float):
        self.events.process_events()
        self.scene_manager.update(dt)

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.scene_manager.draw(self.screen)

        pygame.display.flip()
