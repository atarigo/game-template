import math

from ..component import Character, Collision, PlayerTag, PortalTag, Position, Velocity
from ..core import GameObject
from ..event import EventManager
from ..scene import SceneEvent, SceneEventData
from ..world import WorldManager

BASE_SPEED = 2.4

MIN_AGILITY = 10


def calc_speed(agility: float) -> float:
    multiplier = 2.0  # coefficient of bonus
    divisor = 80  # coefficient of diminishing returns

    bonus = multiplier * math.log(1 + (agility - MIN_AGILITY) / divisor)

    return BASE_SPEED + bonus


class MovementSystem(GameObject):
    def update(self, dt: float, events: EventManager, world: WorldManager) -> None:
        for entity_id in world.get_entities_with(Position, Velocity, Character):
            position = world.get_component(entity_id, Position)
            velocity = world.get_component(entity_id, Velocity)

            character = world.get_component(entity_id, Character)
            speed = calc_speed(character.Agility)

            position.x += velocity.dx * speed
            position.y += velocity.dy * speed

        # get player position and collision
        for entity_id in world.get_entities_with(Position, PlayerTag):
            player_position = world.get_component(entity_id, Position)
            player_collision = world.get_component(entity_id, Collision)
        if not player_position or not player_collision:
            return

        for entity_id in world.get_entities_with(PortalTag, Position):
            portal_position = world.get_component(entity_id, Position)
            portal_collision = world.get_component(entity_id, Collision)

            distance = math.sqrt(
                (player_position.x - portal_position.x) ** 2
                + (player_position.y - portal_position.y) ** 2
            )

            if distance < (player_collision.radius + portal_collision.radius):
                events.emit(SceneEvent.SwitchTo, SceneEventData(name="instance"))
