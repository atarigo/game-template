import pygame
import structlog

from src.plugins.event import EventManager
from src.plugins.scene import SceneBase, SceneEvent

logger = structlog.get_logger(__name__)


class StoreScene(SceneBase):
    def __init__(self, events: EventManager):
        super().__init__(events=events)

    def onkeydown(self, keydown: pygame.event.Event):
        if keydown.key == pygame.K_ESCAPE:
            self.events.emit(SceneEvent.Pop, {})

    def draw(self, screen: pygame.Surface):
        # title
        font = pygame.font.Font(None, 72)
        title = font.render("Store", True, (55, 55, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title, title_rect)
