import pygame

from src.plugins.component import (
    Character,
    Collision,
    DoorTag,
    NameLabel,
    PlayerTag,
    PortalTag,
    Position,
    Sprite,
    Velocity,
)
from src.plugins.core import GameObject
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

    manager.add_component(player, Collision(radius=25))
    image = pygame.Surface((50, 50))
    image.fill((0, 255, 0))
    manager.add_component(player, Sprite(image))

    return player


def create_door(manager: WorldManager, x: int, y: int, name: str = "door"):
    door = manager.create_entity()
    manager.add_component(door, DoorTag())

    manager.add_component(door, Position(x, y))
    manager.add_component(door, NameLabel(name))

    manager.add_component(door, Collision(radius=25))
    image = pygame.Surface((50, 50))
    image.fill((255, 0, 0))
    manager.add_component(door, Sprite(image))
    return door


def create_portal(manager: WorldManager, x: int, y: int, name: str = "portal"):
    portal = manager.create_entity()
    manager.add_component(portal, PortalTag())

    manager.add_component(portal, Position(x, y))
    manager.add_component(portal, NameLabel(name))

    manager.add_component(portal, Collision(radius=25))
    image = pygame.Surface((50, 50))
    image.fill((0, 0, 255))
    manager.add_component(portal, Sprite(image))


class CityLevel1World(GameObject):
    def __init__(self):
        super().__init__()

        self.manager = WorldManager()

        self.player = create_player(self.manager, x=100, y=100)

        self.door = create_door(self.manager, x=200, y=400, name="store")
        self.portal = create_portal(self.manager, x=300, y=400, name="intstance")
