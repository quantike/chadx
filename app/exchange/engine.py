import numpy as np
from loguru import logger

from app.exchange.embedder import Embedder

from .models import Beta, Chad


class MatchingEngine:
    """
    The matching engine takes in a campaign and matches the copy to incoming prompts.
    """

    def __init__(self, chad: Chad) -> None:
        self.chad = chad
        self.embedder = Embedder()
        self.chad_embedding = self.embedder.embed([self.chad.copy])[0]

    async def match(self, beta: Beta):
        """
        Matching algorithm:

        - Embed a beta prompt.
        - If the cosine similarity exceeds the campaign threshold, inject it as a system_prompt
        - If below threshold, no match it made, but fulfill request anyway.
        """
        beta_embedding = self.embedder.embed([beta.prompt])[0]

        similarity = np.dot(beta_embedding, self.chad_embedding) / (
            np.linalg.norm(beta_embedding) * np.linalg.norm(self.chad_embedding)
        )
        logger.info(similarity)

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
