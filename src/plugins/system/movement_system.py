from ..component import Position, Velocity
from ..core import GameObject
from ..world import WorldManager


class MovementSystem(GameObject):
    def update(self, dt: float, world: WorldManager) -> None:
        for entity_id in world.get_entities_with(Position, Velocity):
            position = world.get_component(entity_id, Position)
            velocity = world.get_component(entity_id, Velocity)

            position.x += velocity.dx
            position.y += velocity.dy
