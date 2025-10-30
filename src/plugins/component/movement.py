from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Velocity:
    dx: float
    dy: float
