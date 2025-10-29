import logging

from src.core.game import Game, Settings
from src.core.logs import configure


def main():
    settings = Settings()
    configure(logging.DEBUG)

    game = Game(settings)
    game.run()


if __name__ == "__main__":
    main()
