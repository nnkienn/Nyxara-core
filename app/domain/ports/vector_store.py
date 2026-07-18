from dataclasses import dataclass
from typing import Protocol 
@dataclass

class SearchHit:
    id : str
    text : str
    score : float
class VectorStore(Protocol):
    def upsert(self, tenant_id: str, ids: list[str], texts: list[str], vectors: list[list[float]]) -> None:
        ...

    def search(self, tenant_id: str, query_vector: list[float], top_k: int) -> list[SearchHit]:
        ...