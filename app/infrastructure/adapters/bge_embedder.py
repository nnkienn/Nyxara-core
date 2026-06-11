"""BGEEmbedder — bge-m3 implementation of the ``Embedder`` port.

Loads BAAI/bge-m3 (the single embedding model the project mandates) via
FlagEmbedding. Instantiating this class loads ~4.5GB of weights into RAM, so
build it ONCE per process and reuse it — never per request. Tests use a fake
Embedder instead and never touch the real model.

Note it does NOT ``class BGEEmbedder(Embedder)`` — thanks to ``Protocol``,
having the right ``dim`` + ``embed`` shape is enough to satisfy the port.
"""

from __future__ import annotations

import structlog
from FlagEmbedding import BGEM3FlagModel

logger = structlog.get_logger(__name__)


class BGEEmbedder:
    """bge-m3 embedder (1024-dim, multilingual VN/EN/DE/CN)."""

    DIM = 1024  # bge-m3 dense-vector size

    def __init__(self, model_name: str = "BAAI/bge-m3", *, use_fp16: bool = False) -> None:
        # use_fp16=True only pays off on GPU. Keep False on CPU (the OptiPlex /
        # a Windows dev box) — fp16 on CPU is slower or unsupported.
        logger.info("loading_embedder", model=model_name)
        self._model = BGEM3FlagModel(model_name, use_fp16=use_fp16)

    @property
    def dim(self) -> int:
        return self.DIM

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Encode texts → dense vectors (bge-m3 returns them L2-normalized)."""
        if not texts:  # guard: encode([]) on an empty batch is wasteful / can error
            return []
        dense = self._model.encode(texts, return_dense=True)["dense_vecs"]
        # dense is a numpy 2D array (n_texts × 1024); .tolist() → JSON/Qdrant-friendly.
        return dense.tolist()
