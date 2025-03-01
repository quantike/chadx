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

    async def match(self, beta: Beta) -> Dict[str, str | None] | None:
        user_prompt = beta.prompt
        system_prompt = self.chads.pop(0).prompt if self.chads else None
        
        return {
            # This will never be None
            "user_prompt": user_prompt,

            # This can be None
            "system_prompt": system_prompt,
        }


CHADX = MatchingEngine()
