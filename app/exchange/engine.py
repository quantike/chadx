from typing import Dict, List

from loguru import logger

from .models import Beta, Chad


class MatchingEngine:
    """
    The matching engine takes in a campaign and serves it based on a relevance threshold.
    """

    def __init__(self) -> None:
        self.chads: List[Chad] = []

    async def match(self, beta: Beta) -> Dict[str, str | None] | None:
        user_prompt = beta.prompt
        system_prompt = self.chads.pop(0).copy if self.chads else None
        logger.info("match")
        
        return {
            # This will never be None
            "user_prompt": user_prompt,

            # This can be None
            "system_prompt": system_prompt,
        }
