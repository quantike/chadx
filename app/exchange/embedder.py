import os
from typing import List

from dotenv import load_dotenv
import cohere

load_dotenv()


class Embedder:
    def __init__(self) -> None:
        self.model = "embed-english-v3.0"
        self.input_type = "search_query"
        self.API_KEY = os.getenv("COHERE_API_KEY")
        self.co = cohere.Client(self.API_KEY)

    def embed(self, chunks: List[str]):
        res = self.co.embed(
            texts=chunks,
            model=self.model,
            input_type=self.input_type,
            embedding_types=["float"],
        )
        embedding = res.embeddings.float
        return embedding
