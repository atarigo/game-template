import logging
from pathlib import Path

import pygame
import structlog

from plugins.client import Game
from plugins.core.fonts import install_default_font_override
from plugins.core.logs import configure
from plugins.event import EventManager
from plugins.scene import SceneEvent, SceneEventData, SceneManager

from .scenes import CityScene, InstanceScene, LandingScene, PlaygroundScene, StoreScene
from .setup.config import Settings

logger = structlog.get_logger(__name__)


def prepare(settings: Settings):
    # Set custom default font to jf-openhuninn-2.1.ttf
    font_path = Path("./src/assets/fonts/jf-openhuninn-2.1.ttf")
    if font_path.exists():
        install_default_font_override(font_path)
        logger.info("Font installed", font=font_path)
    else:
        logger.error("Font file not found", font=font_path)

    pygame.init()
    pygame.display.set_mode(settings.window.size)
    pygame.display.set_caption(settings.window.title)


def launch():
    settings = Settings()
    configure(logging.DEBUG)
    prepare(settings)

    prepare()

    events = EventManager()

    scenes = SceneManager(events=events)
    scenes.register("landing", LandingScene)
    scenes.register("city", CityScene)
    scenes.register("store", StoreScene)
    scenes.register("instance", InstanceScene)

    # development
    scenes.register("playground", PlaygroundScene)

    try:
        events.emit(SceneEvent.SwitchTo, SceneEventData(name="landing"))
        game = Game(settings, events, scenes)
        game.run()
    except Exception:
        events.clear()
        pygame.quit()
