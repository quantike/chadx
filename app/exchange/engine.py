from typing import Optional

import numpy as np
from loguru import logger

from app.exchange.embedder import Embedder

from .models import Beta, Chad


class MatchingEngine:
    """
    The matching engine takes in a campaign and matches the copy to incoming prompts.
    """

    def __init__(self, chad: Optional[Chad] = None) -> None:
        self.chad = chad
        self.embedder = Embedder()
        if chad is not None:
            self.chad_embedding = self.embedder.embed([chad.copy])[0]
            self.has_campaign = True
        else:
            self.chad_embedding = None
            self.has_campaign = False

    async def update(self, chad: Chad):
        """
        When a new campaign is created, update the chad in the Matching Engine.
        """
        self.chad = chad
        self.chad_embedding = self.embedder.embed([chad.copy])[0]
        self.has_campaign = True

    async def get(self, id: str) -> Chad | None:
        """
        Get a campaign by ID.
        """
        if self.chad:
            return self.chad if self.chad.id == id else None
        else:
            return None

    async def match(self, beta: Beta):
        """
        Matching algorithm:

        - Embed a beta prompt.
        - If there's no campaign, return the beta object with no match.
        - Otherwise, if the cosine similarity exceeds the campaign threshold,
          inject it as a system_prompt.
        - If below threshold, no match is made, but fulfill the request anyway.
        """
        # Ensure that campaign related actions only occur if a campaign exists.
        if not self.has_campaign or self.chad is None or self.chad_embedding is None:
            logger.info("No campaign available. Skipping matching logic.")
            return {
                "beta": beta,
                "chad": None,
            }

        beta_embedding = self.embedder.embed([beta.prompt])[0]

        similarity = np.dot(beta_embedding, self.chad_embedding) / (
            np.linalg.norm(beta_embedding) * np.linalg.norm(self.chad_embedding)
        )
        logger.info(f"Cosine similarity: {similarity}")

        if similarity >= self.chad.threshold:
            return {
                "beta": beta,
                "chad": self.chad,
            }
        else:
            return {
                "beta": beta,
                "chad": None,
            }
