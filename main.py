import logging

from src.core.logs import configure
from src.main import Game, Settings


def main():
    settings = Settings()
    configure(logging.DEBUG)

    game = Game(settings)
    game.run()


if __name__ == "__main__":
    main()
