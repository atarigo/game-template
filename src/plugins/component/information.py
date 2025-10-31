from dataclasses import dataclass


@dataclass
class NameLabel:
    value: str


@dataclass
class Character:
    Strength: int
    Vitality: int
    Agility: int
    Focus: int
    Intelligence: int
    Willpower: int
