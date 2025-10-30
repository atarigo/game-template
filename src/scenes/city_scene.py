import pygame
import structlog

from src.core.events import EventManager
from src.plugins.scene import SceneBase, SceneEvent

logger = structlog.get_logger(__name__)


class UI:
    def __hash__(self):
        return hash(self.__class__.__name__)

    def __eq__(self, other):
        return (
            isinstance(other, UI)
            and self.__class__.__name__ == other.__class__.__name__
        )

    def onkeydown(self, keydown: pygame.event.Event):
        pass

    def update(self, dt: float):
        pass

    def draw(self, screen: pygame.Surface):
        pass


class Color:
    White = (255, 255, 255)
    Black = (0, 0, 0)
    C = (0, 100, 100)


class InventoryPanel(UI):
    def __init__(self, events: EventManager):
        super().__init__()

        self.events = events

    def onkeydown(self, keydown: pygame.event.Event):
        if keydown.key == pygame.K_u:
            logger.info("use item")

    def draw(self, screen: pygame.Surface):
        window = pygame.Rect((300, 300), (400, 300))
        pygame.draw.rect(screen, Color.White, window)


class CharacterUI(UI):
    def __init__(self, events: EventManager):
        super().__init__()

        self.events = events

    def draw(self, screen: pygame.Surface):
        window = pygame.Rect((100, 300), (100, 300))
        pygame.draw.rect(screen, Color.C, window)


class StoreScene(SceneBase):
    def __init__(self, events: EventManager):
        super().__init__(events=events)

    def onkeydown(self, keydown: pygame.event.Event):
        if keydown.key == pygame.K_ESCAPE:
            self.events.emit("pop", {"scene": "store"})

    def draw(self, screen: pygame.Surface):
        # title
        font = pygame.font.Font(None, 72)
        title = font.render("Store", True, (55, 55, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title, title_rect)


class CityScene(SceneBase):
    def __init__(self, events: EventManager):
        super().__init__(events=events)

        self.UIs: set[UI] = set()

        self.children: list[SceneBase] = []

        self.pause = False

        self.events.subscribe("toggle", self._on_toggle)
        self.events.subscribe("pop", self._on_pop)
        self.events.subscribe("push", self._on_push)

    def _on_push(self, data: dict):
        scene = data.get("scene")
        if scene == "store":
            new_scene = StoreScene(self.events)
            self.children.append(new_scene)
            self.pause = True

    def _on_pop(self, data: dict):
        ui = data.get("ui")
        if ui == "any":
            if self.UIs:
                self.UIs.pop()

        scene = data.get("scene")
        if scene == "store":
            # todo: use pop cause there is only one child now
            self.children.pop()
            self.pause = False

    def _on_toggle(self, data: dict):
        ui = data.get("ui")
        if ui == "item":
            new_ui = InventoryPanel(self.events)
        elif ui == "character":
            new_ui = CharacterUI(self.events)
        else:
            raise ValueError(f"Invalid UI: {ui}")

        if new_ui in self.UIs:
            self.UIs.discard(new_ui)
        else:
            self.UIs.add(new_ui)

    def onkeydown(self, keydown: pygame.event.Event):
        for child in self.children:
            child.onkeydown(keydown)

        if self.pause:
            return

        for ui in self.UIs:
            ui.onkeydown(keydown)

        if keydown.key == pygame.K_i:
            self.events.emit("toggle", {"ui": "item"})

        if keydown.key == pygame.K_c:
            self.events.emit("toggle", {"ui": "character"})

        if keydown.key == pygame.K_f:
            self.events.emit("push", {"scene": "store"})

        if keydown.key == pygame.K_ESCAPE:
            if len(self.UIs) == 0:
                self.events.emit(SceneEvent.SWITCH_TO, {"scene": "landing"})
            else:
                self.events.emit("pop", {"ui": "any"})

    def draw(self, screen: pygame.Surface):
        for child in self.children:
            child.draw(screen)

        if self.pause:
            return

        # title
        font = pygame.font.Font(None, 72)
        title = font.render("City", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title, title_rect)

        for ui in self.UIs:
            ui.draw(screen)
