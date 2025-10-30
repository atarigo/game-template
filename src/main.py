import logging

from .plugins.client import Game
from .plugins.core.logs import configure
from .plugins.event import EventManager
from .plugins.scene import SceneManager
from .scenes import CityScene, LandingScene, StoreScene
from .setup.config import Settings


def launch():
    settings = Settings()
    configure(logging.DEBUG)

    events = EventManager()

    scenes = SceneManager(events=events)
    scenes.register("landing", LandingScene)
    scenes.register("city", CityScene)
    scenes.register("store", StoreScene)

    game = Game(settings, events, scenes)
    game.run()
