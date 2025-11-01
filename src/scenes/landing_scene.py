import pygame
import pygame_gui
import structlog

from src.plugins.client import GameEvent
from src.plugins.event import EventManager
from src.plugins.scene import SceneBase, SceneEvent, SceneEventData

logger = structlog.get_logger(__name__)

font = {
    "name": "jf-openhuninn",
    "regular_path": "./src/assets/fonts/jf-openhuninn-2.1.ttf",
}

theme = {
    "button": {"font": font},
    "label": {"font": font},
}


class UIManager:
    def __init__(self, events: EventManager):
        self.events = events

        screen = pygame.display.get_surface()
        self.manager = pygame_gui.UIManager(screen.get_size(), theme)

        # 置中配置：以視窗中心為錨點，使用相對位移維持垂直間距
        self.new_game_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 230), (200, 50)),
            text="新遊戲",
            manager=self.manager,
            anchors={"centerx": "centerx", "top": "top"},
        )
        self.playground_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 300), (200, 50)),
            text="Playground",
            manager=self.manager,
            anchors={"centerx": "centerx", "top": "top"},
        )
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 370), (200, 50)),
            text="Quit",
            manager=self.manager,
            anchors={"centerx": "centerx", "top": "top"},
        )

    def handle_event(self, event: pygame.event.Event):
        # 視窗尺寸變更時通知 UIManager 重新計算 anchored 佈局
        if event.type == pygame.VIDEORESIZE:
            self.manager.set_window_resolution(event.size)
        self.manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.new_game_button:
                self.events.emit(SceneEvent.SwitchTo, SceneEventData(name="city"))
            elif event.ui_element == self.playground_button:
                self.events.emit(SceneEvent.SwitchTo, SceneEventData(name="playground"))
            elif event.ui_element == self.quit_button:
                self.events.emit(GameEvent.Quitting)

    def update(self, dt: float):
        self.manager.update(dt)

    def draw(self, screen: pygame.Surface):
        self.manager.draw_ui(screen)


class LandingScene(SceneBase):
    def __init__(self, events: EventManager):
        super().__init__(events=events)

        self.ui_manager = UIManager(self.events)

    def onkeydown(self, keydown: pygame.event.Event):
        if keydown.key == pygame.K_ESCAPE:
            self.events.emit(GameEvent.Quitting)

    def handle_event(self, event: pygame.event.Event):
        self.ui_manager.handle_event(event)

        super().handle_event(event)

    def update(self, dt: float):
        self.ui_manager.update(dt)

    def draw(self, screen: pygame.Surface):
        self.ui_manager.draw(screen)

        # title
        title = pygame.font.Font(None, 72).render("ECS Game", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title, title_rect)

        # hint
        hint = pygame.font.Font(None, 36).render(
            "Use Arrow Keys + Enter", True, (150, 150, 150)
        )
        hint_rect = hint.get_rect(center=(screen.get_width() // 2, 500))
        screen.blit(hint, hint_rect)
