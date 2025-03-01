from typing import List

import torch
from loguru import logger
from numpy import float32
from numpy.typing import NDArray
from sentence_transformers import SentenceTransformer


class Embedder:
    """
    The `Embedder` defines a `MODEL` and must use those model params to initialize the model and provide
    and embedding functionality.
    """

    MODEL_NAME = "answerdotai/ModernBERT-base"
    MODEL_DIM = 768
    MODEL_CONTEXT = 8192

    def __init__(self, truncate_dim: int | None = None) -> None:
        """
        Initialize the Embedder with model parameters.

        Args:
            truncate_dim (Optional[int]): Dimension to truncate the model to.
        """
        # NOTE: Fugly, I know.
        logger.info(f"Creating vector embeddings with: {self.MODEL_NAME}")
        assert truncate_dim > self.MODEL_DIM if truncate_dim else True, "Truncation exceeds model dimensionality"

        # Check if GPU is available and use it
        if torch.cuda.is_available():
            device = "cuda"
            torch.set_float32_matmul_precision("high")
        else:
            device = "cpu"
        logger.info(f"Using device: {device}")

        self.model = SentenceTransformer(self.MODEL_NAME, truncate_dim=truncate_dim if truncate_dim else self.MODEL_DIM)

    def embed(self, chunks: List[str], progress: bool = False) -> NDArray[float32]:
        """
        Embed the given chunks of text.

        Args:
            chunks (List[str]): List of text chunks to embed.
            progress (bool): Whether to show progress bar.

        Returns:
            NDArray: Embeddings of the text chunks.
        """
        return self.model.encode(chunks, show_progress_bar=progress)

