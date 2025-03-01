import csv
import os
from datetime import datetime
from typing import List, Optional

import numpy as np
from loguru import logger

from app.exchange.embedder import Embedder

from .models import Beta, Chad


class MatchingEngine:
    """
    The matching engine takes in a prompt (beta) and matches it to the most similar campaign (chad)
    from a list of campaigns. A campaign is only considered a match if the cosine similarity between
    the prompt and the campaign copy exceeds the campaign's threshold.
    """

    def __init__(self) -> None:
        self.chads: List[Chad] = []
        self.chad_embeddings = {}  # mapping from chad.id to its embedding
        self.embedder = Embedder()

        # CSV File Setup: now including a column for whether the campaign was chosen as a match.
        self.csv_file = "matches.csv"
        if os.path.exists(self.csv_file):
            os.remove(self.csv_file)
        with open(self.csv_file, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["impressions", "chad_id", "similarity", "matched", "timestamp"])

    def _embed_chad(self, chad: Chad):
        """Embed a single campaign copy and return the embedding."""
        embedding = self.embedder.embed([chad.copy])[0]
        return embedding

    async def put(self, chad: Chad):
        """
        Add a new campaign to the matching engine.
        Validate the campaign, compute its embedding, and store it.
        """
        # Validate campaign parameters
        if not (0 <= chad.threshold <= 1):
            return None
        if not (0 <= chad.tier <= 2):
            return None
        if not (0 <= chad.budget <= 1000000):
            return None

        # Ensure the Chad has an impressions attribute.
        if not hasattr(chad, "impressions"):
            chad.impressions = 0

        self.chads.append(chad)
        self.chad_embeddings[chad.id] = self._embed_chad(chad)

    async def get(self, id: str) -> Optional[Chad]:
        """
        Get a campaign by ID.
        """
        for chad in self.chads:
            if chad.id == id:
                return chad
        return None

    async def delete(self, id: str) -> Optional[str]:
        """
        Delete a campaign by ID.
        """
        for i, chad in enumerate(self.chads):
            if chad.id == id:
                self.chads.pop(i)
                self.chad_embeddings.pop(chad.id, None)
                return id
        return None

    async def match(self, beta: Beta):
        """
        Matching algorithm for multiple campaigns:
        
        - Embed the beta prompt.
        - Iterate over each campaign and compute cosine similarity.
        - Select the campaign with the highest similarity that meets its threshold.
        - If a match is found, increment its impressions.
        - Log each campaign's similarity evaluation and whether it was chosen.
        """
        if not self.chads:
            logger.info("No campaigns available. Skipping matching logic.")
            return {
                "beta": beta,
                "chad": None,
            }

        beta_embedding = self.embedder.embed([beta.prompt])[0]

        best_match = None
        best_similarity = -1  # initialize with a very low similarity
        evaluations = []  # list to store evaluation results: (chad, similarity)

        for chad in self.chads:
            chad_embedding = self.chad_embeddings[chad.id]
            similarity = np.dot(beta_embedding, chad_embedding) / (
                np.linalg.norm(beta_embedding) * np.linalg.norm(chad_embedding)
            )
            logger.info(f"Chad {chad.id} similarity: {similarity}")
            evaluations.append((chad, similarity))
            if similarity >= chad.threshold and similarity > best_similarity:
                best_similarity = similarity
                best_match = chad

        # Only increment impressions for the chosen campaign if there's a match.
        if best_match:
            best_match.impressions += 1

        # Log every campaign's evaluation to CSV.
        for chad, similarity in evaluations:
            matched = (chad == best_match)
            self.write_match_to_csv(chad, similarity, matched)

        if best_match:
            logger.info(
                f"Match found: Chad {best_match.id} with similarity {best_similarity}, impressions={best_match.impressions}"
            )
            return {
                "beta": beta,
                "chad": best_match,
            }
        else:
            return {
                "beta": beta,
                "chad": None,
            }

    def write_match_to_csv(self, chad: Chad, similarity: float, matched: bool):
        """
        Write an evaluation entry to CSV with the campaign's current impression count, campaign id,
        similarity, match flag, and the current timestamp.
        """
        timestamp = datetime.now().isoformat()
        with open(self.csv_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([chad.impressions, chad.id, similarity, matched, timestamp])

