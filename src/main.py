import logging

from .core.events import EventManager
from .core.game import Game, Settings
from .core.logs import configure
from .core.scenes import SceneManager
from .scenes import CityScene, LandingScene


def launch():
    settings = Settings()
    configure(logging.DEBUG)

    events = EventManager()

    scenes = SceneManager(events=events)
    scenes.register("landing", LandingScene)
    scenes.register("city", CityScene)

    game = Game(settings, events, scenes)
    game.run()
