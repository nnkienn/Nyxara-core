from typing import Protocol

class Embedder(Protocol):
    dim : int
    def embed(self, texts: list[str]) -> list[list[float]]:
        ...