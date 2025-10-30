import pygame

from ..component import Position, Sprite
from ..core import GameObject
from ..world import WorldManager


class RenderSystem(GameObject):
    def draw(self, screen: pygame.Surface, world: WorldManager) -> None:
        for entity_id in world.get_entities_with(Position, Sprite):
            pos = world.get_component(entity_id, Position)
            sprite = world.get_component(entity_id, Sprite)

            # center align
            x = pos.x - sprite.width // 2
            y = pos.y - sprite.height // 2
            screen.blit(sprite.image, (x, y))
