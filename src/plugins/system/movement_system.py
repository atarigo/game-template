import math

from ..component import Character, Position, Velocity
from ..core import GameObject
from ..world import WorldManager

BASE_SPEED = 2.4

MIN_AGILITY = 10


def calc_speed(agility: float) -> float:
    multiplier = 2.0  # coefficient of bonus
    divisor = 80  # coefficient of diminishing returns

    bonus = multiplier * math.log(1 + (agility - MIN_AGILITY) / divisor)

    return BASE_SPEED + bonus


class MovementSystem(GameObject):
    def update(self, dt: float, world: WorldManager) -> None:
        for entity_id in world.get_entities_with(Position, Velocity, Character):
            position = world.get_component(entity_id, Position)
            velocity = world.get_component(entity_id, Velocity)

            character = world.get_component(entity_id, Character)
            speed = calc_speed(character.Agility)

            position.x += velocity.dx * speed
            position.y += velocity.dy * speed
