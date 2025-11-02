import logging

import pygame

from plugins.client import Game
from plugins.core.logs import configure
from plugins.event import EventManager
from plugins.scene import SceneEvent, SceneEventData, SceneManager

from .scenes import CityScene, InstanceScene, LandingScene, PlaygroundScene, StoreScene
from .setup.config import Settings


def prepare(settings):
    pygame.init()
    pygame.display.set_mode(settings.window.size)
    pygame.display.set_caption(settings.window.title)


def launch():
    settings = Settings()
    configure(logging.DEBUG)
    prepare(settings)

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
