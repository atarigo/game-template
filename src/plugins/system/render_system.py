import pygame

from ..component import NameLabel, Position, Sprite
from ..core import GameObject
from ..world import WorldManager


class RenderSystem(GameObject):
    def __init__(self):
        self.lable_font = pygame.font.Font(None, 24)

    def draw(self, screen: pygame.Surface, world: WorldManager) -> None:
        for entity_id in world.get_entities_with(Position, Sprite):
            pos = world.get_component(entity_id, Position)
            sprite = world.get_component(entity_id, Sprite)

            # center align
            x = pos.x - sprite.width // 2
            y = pos.y - sprite.height // 2
            screen.blit(sprite.image, (x, y))

            # label
            name_label = world.get_component(entity_id, NameLabel)
            if name_label:
                text = self.lable_font.render(name_label.value, True, (255, 255, 255))

                text_rect = text.get_rect(
                    midtop=(pos.x, pos.y + sprite.height // 2 + 8)
                )
                screen.blit(text, text_rect)
