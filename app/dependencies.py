# The database
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Beta:
    prompt: str


@dataclass
class Chad:
    id: str
    tier: int
    prompt: str


class MatchingEngine:

    def __init__(self) -> None:
        self.chads: List[Chad] = []
        self.betas: List[Beta] = []

    def match(self) -> Dict[str, str | None] | None:
        # Ensure there is at least one element in each list
        if not self.betas:
            return None

        user_prompt = self.betas.pop(0).prompt
        system_prompt = self.chads.pop(0).prompt if self.chads else None
        
        return {
            # This will never be None
            "user_prompt": user_prompt,

            # This can be None
            "system_prompt": system_prompt,
        }


CHADX = MatchingEngine()
