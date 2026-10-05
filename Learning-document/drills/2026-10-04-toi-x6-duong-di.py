# TỐI 04/10 — X6: in ĐƯỜNG ĐI của MỘT cây qua cả hệ thống lát 0. Chỉ đọc, không gõ.
# Chạy: PYTHONPATH=. .venv/bin/python Learning-document/drills/2026-10-04-toi-x6-duong-di.py
from qdrant_client import QdrantClient

import app.application.retrieval.bm25_index as bm25_mod
import app.application.retrieval.hybrid_retriever as hybrid_mod
import app.infrastructure.adapters.vectorstore.qdrant_store as qstore_mod
from app.application.retrieval.bm25_index import BM25Index
from app.application.retrieval.hybrid_retriever import HybridRetriever
from app.infrastructure.adapters.vectorstore.qdrant_store import QdrantStore

V = [1.0, 0.0, 0.0]
CORPUS_A = [
    ("vb1", "Nghị định về thuế thu nhập", {"loai": "Nghị định", "nam": 2020}),
    ("vb2", "Nghị định về đất đai", {"loai": "Nghị định", "nam": 2010}),
    ("vb3", "Luật về thuế giá trị gia tăng", {"loai": "Luật", "nam": 2016}),
    ("vb4", "Luật doanh nghiệp", {"loai": "Luật", "nam": 2020}),
    ("vb5", "Thông tư hướng dẫn về thuế", {"loai": "Thông tư", "nam": 2021}),
]


class FakeEmbedder:
    dim = 3

    def embed(self, texts):
        return [V for _ in texts]


# ── gắn "camera" vào 2 hàm CỦA BẠN + RRF, để in ra lúc chúng được gọi ──
_real_to_qdrant = qstore_mod.to_qdrant_filter
_real_matches = bm25_mod.matches
_real_rrf = hybrid_mod.reciprocal_rank_fusion


def cam_to_qdrant(tree):
    out = _real_to_qdrant(tree)
    print(f"  [2a] to_qdrant_filter (CỦA BẠN) dịch cây -> {out}")
    return out


def cam_matches(tree, meta):
    out = _real_matches(tree, meta)
    print(f"  [2b] matches (CỦA BẠN) chấm {meta} -> {out}")
    return out


def cam_rrf(lists, **kw):
    print(f"  [3]  RRF nhận 2 danh sách: dense={lists[0]}  bm25={lists[1]}")
    return _real_rrf(lists, **kw)


qstore_mod.to_qdrant_filter = cam_to_qdrant
bm25_mod.matches = cam_matches
hybrid_mod.reciprocal_rank_fusion = cam_rrf

store = QdrantStore(client=QdrantClient(location=":memory:"), collection="legal", dim=3)
bm25 = BM25Index()
store.upsert("A", [d for d, _, _ in CORPUS_A], [t for _, t, _ in CORPUS_A], [V] * 5, [m for _, _, m in CORPUS_A])
for d, t, m in CORPUS_A:
    bm25.add_document("A", d, t, m)
retriever = HybridRetriever(FakeEmbedder(), store, bm25)

tree = {"eq": ["loai", "Nghị định"]}
print(f"[1]  Người dùng tenant A hỏi 'thuế', gửi cây: {tree}")
print("     HybridRetriever chuyền NGUYÊN cây này xuống 2 nhánh:")
result = retriever.search("A", "thuế", top_k=10, filter_tree=tree)
print(f"[4]  Kết quả cuối: {[d for d, _ in result]}")
