import pygame

from src.plugins.component import Position, Sprite
from src.plugins.world import WorldManager


def create_player(manager: WorldManager, x: int, y: int):
    player = manager.create_entity()

    manager.add_component(player, Position(x, y))

    image = pygame.Surface((50, 50))
    image.fill((0, 255, 0))
    manager.add_component(player, Sprite(image))

    return player


def create_door(manager: WorldManager, x: int, y: int):
    door = manager.create_entity()

    manager.add_component(door, Position(x, y))

    image = pygame.Surface((50, 50))
    image.fill((255, 0, 0))
    manager.add_component(door, Sprite(image))
    return door


class CityLevel1World:
    def __init__(self):
        self.manager = WorldManager()

        self.player = create_player(self.manager, x=100, y=100)
        self.door = create_door(self.manager, x=200, y=200)
