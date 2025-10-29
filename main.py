from src.main import Game, Settings


def main():
    settings = Settings()

    game = Game()
    game.setup(settings)
    game.run()


if __name__ == "__main__":
    main()
