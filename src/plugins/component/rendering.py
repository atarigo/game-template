from dataclasses import dataclass

import pygame


@dataclass
class Sprite:
    image: pygame.Surface
    width: int = 0
    height: int = 0

    def __post_init__(self):
        if self.width == 0:
            self.width = self.image.get_width()
        if self.height == 0:
            self.height = self.image.get_height()
