import pygame

from src.plugins.event import EventManager
from src.plugins.scene import SceneBase

from ..plugins.system import MovementSystem, PlayerControlSystem, RenderSystem
from ..worlds.instances.v1 import BloodMoonForestWorld


def random_world():
    return BloodMoonForestWorld()


class InstanceScene(SceneBase):
    def __init__(self, events: EventManager):
        super().__init__(events=events)

        self.world = random_world()

        self.systems = [
            PlayerControlSystem(),
            MovementSystem(),
            RenderSystem(),
        ]

    def update(self, dt: float):
        self.world.update(dt)

        for system in self.systems:
            system.update(dt, self.events, self.world.manager)

    def draw(self, screen: pygame.Surface):
        for system in self.systems:
            system.draw(screen, self.world.manager)
