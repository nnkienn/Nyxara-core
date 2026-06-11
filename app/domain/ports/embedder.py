"""Embedder port — the interface the RAG pipeline depends on.

Hexagonal note
--------------
This lives in ``domain`` because the core defines WHAT it needs ("turn text
into vectors"), never HOW. Concrete implementations (adapters) live in
``app/infrastructure/adapters/``. The domain must NOT import FlagEmbedding /
torch — only this abstract contract.

Why a real port here (unlike ``LLMClientBase``, a single config-swap wrapper in
``core``)? Because embedding backends are genuinely different APIs — bge-m3
(local, FlagEmbedding) vs OpenAI embeddings (HTTP) share no protocol. The port
lets the pipeline swap them without changing a single caller.
"""

from __future__ import annotations

from typing import Protocol


class Embedder(Protocol):
    """Turns text into dense vectors.

    This is a ``Protocol`` (structural typing): *any* object that has a ``dim``
    property and an ``embed`` method IS an ``Embedder`` — the adapter does NOT
    need to inherit from this class. Type checkers verify the shape; at runtime
    it's plain duck typing.
    """

    @property
    def dim(self) -> int:
        """Vector dimensionality (e.g. 1024 for bge-m3).

        The vector store reads this to size its collection, so the dimension is
        never hardcoded downstream — change the model, the collection follows.
        """
        ...

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts → one vector per text, in the same order.

        Vectors are L2-normalized (length 1), so cosine similarity == dot
        product — the property you proved by hand in the Phase-2 prototype.
        """
        ...
