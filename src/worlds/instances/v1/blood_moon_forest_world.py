import math
import random

import pygame
import structlog

from plugins.component import (
    Character,
    EnemyTag,
    NameLabel,
    PlayerTag,
    Position,
    Sprite,
    Velocity,
)
from plugins.core import GameObject
from plugins.world import WorldManager

logger = structlog.get_logger()


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


def create_enemy(manager: WorldManager, x: int, y: int, name: str):
    logger.debug("create enemy", name=name, x=x, y=y)

    enemy = manager.create_entity()
    manager.add_component(enemy, EnemyTag())
    manager.add_component(
        enemy,
        Character(
            Strength=20,
            Vitality=30,
            Agility=20,
            Focus=10,
            Intelligence=3,
            Willpower=10,
        ),
    )

    manager.add_component(enemy, Position(x, y))
    manager.add_component(enemy, NameLabel(name))

    image = pygame.Surface((50, 50))
    image.fill((255, 0, 0))
    manager.add_component(enemy, Sprite(image))
    return enemy


class Blackboard:
    def __init__(self):
        self.elapsed = 30
        self.stage = 1


class BloodMoonForestWorld(GameObject):
    name: str = "Blood Moon Forest"  # 血月叢林

    def __init__(self):
        super().__init__()

        self.manager = WorldManager()

        self.start_position = (100, 100)
        self.player = create_player(self.manager, x=100, y=100)

        self.blackboard = Blackboard()

    def create_werewolf(self):
        enemies = self.manager.get_entities_with(Position, EnemyTag)
        diff_count = int((self.blackboard.elapsed / 60) - len(enemies))
        if diff_count <= 0:
            return

        for entity_id in self.manager.get_entities_with(Position, PlayerTag):
            player_position = self.manager.get_component(entity_id, Position)

        if not player_position:
            return

        for _ in range(diff_count):
            # 在玩家周邊 400-800 像素的環形區域內隨機生成
            angle = random.uniform(0, 2 * math.pi)  # 隨機角度
            distance = random.uniform(400, 800)  # 隨機距離 400-800 像素
            offset_x = int(distance * math.cos(angle))
            offset_y = int(distance * math.sin(angle))

            create_enemy(
                x=player_position.x + offset_x,
                y=player_position.y + offset_y,
                name="werewolf",
                manager=self.manager,
            )

    def finish_stage_1(self):
        euclidean_distance = math.sqrt(
            (self.player.x - self.start_position.x) ** 2
            + (self.player.y - self.start_position.y) ** 2
        )
        if euclidean_distance > 1000:
            self.blackboard.stage = 2

    def update(self, dt: float):
        self.blackboard.elapsed += dt

        if self.blackboard.stage == 1:
            self.create_werewolf()

        if self.blackboard.stage == 2:
            pass
