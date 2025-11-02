from dataclasses import dataclass, field


@dataclass
class Window:
    size: tuple[int, int] = (800, 600)
    title: str = "Pygame Plugins"


@dataclass
class Settings:
    window: Window = field(default_factory=Window)
