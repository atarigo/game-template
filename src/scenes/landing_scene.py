import pygame
import structlog

from src.core.events import EventManager
from src.plugins.scene import SceneBase, SceneEvent
from src.state import GameState

logger = structlog.get_logger(__name__)


class LandingScene(SceneBase):
    def __init__(self, events: EventManager):
        super().__init__(events=events)

        self.selected: int = 0
        self.options: list[str] = ["New Game", "Quit"]

    def on_enter(self):
        self.selected = 0

    def on_exit(self):
        logger.info("exit to landing scene")

    def onkeydown(self, keydown: pygame.event.Event):
        if keydown.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.options)
        elif keydown.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.options)
        elif keydown.key == pygame.K_ESCAPE:
            self.events.emit(GameState.Quitting)
        elif keydown.key == pygame.K_RETURN:
            if self.selected == 0:
                self.events.emit(SceneEvent.SWITCH_TO, {"scene": "city"})
            elif self.selected == 1:
                self.events.emit(GameState.Quitting)

    def draw(self, screen: pygame.Surface):
        # title
        title = pygame.font.Font(None, 72).render("ECS Game", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title, title_rect)

        # options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (200, 200, 200)
            text = pygame.font.Font(None, 36).render(option, True, color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, 300 + i * 60))
            screen.blit(text, text_rect)

        # hint
        hint = pygame.font.Font(None, 36).render(
            "Use Arrow Keys + Enter", True, (150, 150, 150)
        )
        hint_rect = hint.get_rect(center=(screen.get_width() // 2, 500))
        screen.blit(hint, hint_rect)
