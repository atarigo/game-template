import logging
from dataclasses import dataclass, field
from enum import Enum, auto

import pygame

from src.core.events import EventManager

logger = logging.getLogger(__name__)


@dataclass
class Window:
    size: tuple[int, int] = (800, 600)
    title: str = "Pygame Plugins"


@dataclass
class Settings:
    window: Window = field(default_factory=Window)


class GameState(Enum):
    Running = auto()
    Quitting = auto()


class Game:
    def __init__(self):
        pygame.init()

        self.state: GameState = GameState.Running

        # Managers
        self.events = EventManager()
        self.events.subscribe("game quit", self.teardown)

    def __exit__(self):
        logger.debug("Quitting game")

        self.events.clear()
        pygame.quit()

    def setup(self, settings: Settings):
        self.screen = pygame.display.set_mode(settings.window.size)
        pygame.display.set_caption(settings.window.title)

    def teardown(self, *args, **kwargs):
        self.state = GameState.Quitting

    def run(self):
        while self.state == GameState.Running:
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.events.emit("game quit")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.events.emit("game quit")

    def update(self):
        self.events.process_events()

    def draw(self):
        self.screen.fill((0, 0, 0))

        pygame.display.flip()
