from pathlib import Path

import pygame


def install_default_font_override(font_path: str | Path) -> None:
    """Install a global override so Font(None, size) uses the given TTF."""
    pygame.font.init()

    original_ctor = pygame.font.Font

    def _font_ctor(name, size, *args, **kwargs):
        if name is None:
            return original_ctor(str(font_path), size, *args, **kwargs)
        return original_ctor(name, size, *args, **kwargs)

    pygame.font.Font = _font_ctor
