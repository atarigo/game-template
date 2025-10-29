from enum import Enum

import pygame
import structlog

from .core.events import EventManager
from .setup.config import Settings

logger = structlog.get_logger(__name__)


class GameState(Enum):
    Running = "GameRunning"
    Quitting = "GameQuitting"


class GameStateManager:
    def __init__(self, events: EventManager):
        self.current: GameState = GameState.Running

        events.subscribe(GameState.Quitting, self.game_quit_handler)

    def game_quit_handler(self, *args, **kwargs):
        self.current = GameState.Quitting


class Game:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.events = EventManager()

        # managers
        self.state = GameStateManager(events=self.events)

        # initialize pygame
        logger.info("Game initialized")
        pygame.init()
        pygame.display.set_mode(settings.window.size)
        pygame.display.set_caption(settings.window.title)

        self.screen = pygame.display.get_surface()

    def __del__(self):
        logger.info("Game destroyed")
        self.events.clear()
        pygame.quit()

    def run(self):
        while self.state.current == GameState.Running:
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.events.emit(GameState.Quitting)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.events.emit(GameState.Quitting)

    def update(self):
        self.events.process_events()

    def draw(self):
        self.screen.fill((0, 0, 0))

        pygame.display.flip()
