import pygame
import structlog

from src.core.events import EventManager
from src.scenes.events import SceneEvent

from .base import Scene

logger = structlog.get_logger(__name__)


class CityScene(Scene):
    def __init__(self, events: EventManager):
        super().__init__(events=events)

    def on_enter(self):
        logger.info("CityScene on_enter")

        logger.debug("world initialized")
        logger.debug("user entity created")

    def on_exit(self):
        logger.info("enter to whatever scene")

    def handle_event(self, keydown: pygame.event.Event):
        if keydown.key == pygame.K_UP:
            logger.info("move up")
        elif keydown.key == pygame.K_DOWN:
            logger.info("move down")
        elif keydown.key == pygame.K_LEFT:
            logger.info("move left")
        elif keydown.key == pygame.K_RIGHT:
            logger.info("move right")
        elif keydown.key == pygame.K_ESCAPE:
            self.events.emit(SceneEvent.SWITCH_TO, {"scene": "landing"})

    def draw(self, screen: pygame.Surface):
        # title
        font = pygame.font.Font(None, 72)
        title = font.render("City", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title, title_rect)
