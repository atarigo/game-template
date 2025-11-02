from typing import TYPE_CHECKING

import pygame
import structlog

from ..scene import SceneEvent, SceneEventData
from .events import GameEvent, GameStateManager

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
        self.settings = settings
        self.events = events
        self.scene_manager = scene_manager

        self.state = GameStateManager(events=events)

        # initialize pygame
        logger.info("Game initialized")
        pygame.init()
        pygame.display.set_mode(settings.window.size)
        pygame.display.set_caption(settings.window.title)

        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        # Initialize first scene
        self.events.emit(SceneEvent.SwitchTo, SceneEventData(name="landing"))

    def __del__(self):
        logger.info("Game destroyed")
        self.events.clear()
        pygame.quit()

    def run(self):
        while self.state.current == GameEvent.Running:
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
