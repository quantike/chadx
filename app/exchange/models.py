from dataclasses import dataclass


@dataclass
class Beta:
    prompt: str


@dataclass
class Chad:
    id: str
    copy: str
    budget: int
    tier: int
    threshold: float
