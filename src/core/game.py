import pygame
import structlog

from src.setup.config import Settings
from src.state import GameState, GameStateManager, SceneState

from .events import EventManager
from .scenes import SceneManager

logger = structlog.get_logger(__name__)


class Game:
    def __init__(self, settings: Settings, events: EventManager, scenes: SceneManager):
        self.settings = settings
        self.events = events
        self.scenes = scenes

        self.state = GameStateManager(events=events)

        # initialize pygame
        logger.info("Game initialized")
        pygame.init()
        pygame.display.set_mode(settings.window.size)
        pygame.display.set_caption(settings.window.title)

        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.events.emit(SceneState.SwitchTo, {"scene_name": "landing"})

    def __del__(self):
        logger.info("Game destroyed")
        self.events.clear()
        pygame.quit()

    def run(self):
        while self.state.current == GameState.Running:
            dt = self.clock.tick(60) / 1000  # seconds

            self.handle_events()
            self.update(dt)
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.events.emit(GameState.Quitting)

            if event.type == pygame.KEYDOWN:
                self.scenes.handle_event(keydown=event)

    def update(self, dt: float):
        self.events.process_events()
        self.scenes.update(dt)

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.scenes.draw(self.screen)

        pygame.display.flip()
