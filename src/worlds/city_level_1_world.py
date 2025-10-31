import pygame

from src.plugins.component import (
    Character,
    NameLabel,
    PlayerTag,
    Position,
    Sprite,
    Velocity,
)
from src.plugins.world import WorldManager


def create_player(manager: WorldManager, x: int, y: int, name: str = "player"):
    player = manager.create_entity()
    manager.add_component(player, PlayerTag())
    manager.add_component(
        player,
        Character(
            Strength=10,
            Vitality=10,
            Agility=10,
            Focus=10,
            Intelligence=10,
            Willpower=10,
        ),
    )

    manager.add_component(player, Position(x, y))
    manager.add_component(player, Velocity(0, 0))
    manager.add_component(player, NameLabel(name))

    image = pygame.Surface((50, 50))
    image.fill((0, 255, 0))
    manager.add_component(player, Sprite(image))

    return player


def create_door(manager: WorldManager, x: int, y: int, name: str = "door"):
    door = manager.create_entity()

    manager.add_component(door, Position(x, y))
    manager.add_component(door, NameLabel(name))

    image = pygame.Surface((50, 50))
    image.fill((255, 0, 0))
    manager.add_component(door, Sprite(image))
    return door


class CityLevel1World:
    def __init__(self):
        self.manager = WorldManager()

        self.player = create_player(self.manager, x=100, y=100)
        self.door = create_door(self.manager, x=200, y=400, name="store")
        self.portal = create_door(self.manager, x=300, y=400, name="intstance")
