from dataclasses import dataclass
from typing import Optional, Protocol
@dataclass

class SearchHit:
    id : str
    text : str
    score : float
class VectorStore(Protocol):
    # metadatas[i] = metadata của ids[i] (vd {"loai": "Nghị định", "nam": 2020}). None = không có.
    def upsert(
        self,
        tenant_id: str,
        ids: list[str],
        texts: list[str],
        vectors: list[list[float]],
        metadatas: Optional[list[dict]] = None,
    ) -> None:
        ...

    # filter_tree = cây điều kiện TRUNG LẬP ({"and": [...]}, {"eq": [field, value]}...),
    # KHÔNG phải dict Qdrant. Mỗi adapter tự dịch sang giọng của kho mình (chốt X3, 02/10).
    def search(
        self,
        tenant_id: str,
        query_vector: list[float],
        top_k: int,
        filter_tree: Optional[dict] = None,
    ) -> list[SearchHit]:
        ...
    def delete(self, tenant_id: str, doc_id: str) -> None:
        ...