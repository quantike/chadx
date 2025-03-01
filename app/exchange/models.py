from dataclasses import dataclass


@dataclass
class Beta:
    prompt: str


@dataclass
class Chad:
    id: str
    copy: str
    budget: int
    tier: int = 0
    threshold: float = 0.2
    impressions: int = 0
