import pygame
import structlog

from src.plugins.event import EventManager
from src.plugins.scene import (
    SceneBase,
    SceneEvent,
    SceneEventData,
    UIBase,
    UIEvent,
    UIEventData,
    UIManager,
)
from src.plugins.system import RenderSystem
from src.worlds import CityLevel1World

logger = structlog.get_logger(__name__)


class Color:
    White = (255, 255, 255)
    Black = (0, 0, 0)
    C = (0, 100, 100)


class InventoryPanel(UIBase):
    def __init__(self, events: EventManager):
        super().__init__(events=events)

    def onkeydown(self, keydown: pygame.event.Event):
        if keydown.key == pygame.K_u:
            logger.info("use item")

    def draw(self, screen: pygame.Surface):
        window = pygame.Rect((300, 300), (400, 300))
        pygame.draw.rect(screen, Color.White, window)


class CharacterPanel(UIBase):
    def __init__(self, events: EventManager):
        super().__init__(events=events)

    def draw(self, screen: pygame.Surface):
        window = pygame.Rect((100, 300), (100, 300))
        pygame.draw.rect(screen, Color.C, window)


class CityScene(SceneBase):
    def __init__(self, events: EventManager):
        super().__init__(events=events)

        self.ui_manager = UIManager(events=self.events)
        self.ui_manager.register("inventory", InventoryPanel)
        self.ui_manager.register("character", CharacterPanel)

        self.world = CityLevel1World()

        self.systems = [
            RenderSystem(),
        ]

        self.pause = False

    def onkeydown(self, keydown: pygame.event.Event):
        if self.pause:
            return

        self.ui_manager.handle_event(event=keydown)

        if keydown.key == pygame.K_i:
            self.events.emit(UIEvent.Toggle, UIEventData(name="inventory"))
        elif keydown.key == pygame.K_c:
            self.events.emit(UIEvent.Toggle, UIEventData(name="character"))
        elif keydown.key == pygame.K_f:
            # todo: delete it, this is a fake event for testing
            self.events.emit(SceneEvent.Append, SceneEventData(name="store"))
        elif keydown.key == pygame.K_ESCAPE:
            if self.ui_manager.children:
                self.events.emit(UIEvent.Pop, None)
            else:
                self.events.emit(SceneEvent.SwitchTo, SceneEventData(name="landing"))

    def update(self, dt: float):
        for system in self.systems:
            system.update(dt)

    def draw(self, screen: pygame.Surface):
        for system in self.systems:
            system.draw(screen, self.world.manager)

        if self.pause:
            return

        # title
        font = pygame.font.Font(None, 72)
        title = font.render("City", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title, title_rect)

        self.ui_manager.draw(screen)
