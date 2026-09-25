"""
Máy đo — KHÔNG chứa logic lõi. Nó chỉ gọi `ingest_document` THẬT và in ra
trạng thái thật sau mỗi kịch bản.

Cách dùng (bắt buộc): TRƯỚC mỗi lần bấm Enter, nói ra dự đoán của bạn.
    .venv/bin/python Learning-document/drills/2026-09-09-manifest-vs-kho.py
"""
from app.application.ingestion.pipeline import ingest_document
from app.application.retrieval.bm25_index import BM25Index


class FakeDocStore:
    def __init__(self): self.data = {}
    def save(self, t, i, text): self.data[(t, i)] = text
    def get(self, t, i): return self.data[(t, i)]
    def delete(self, t, i): self.data.pop((t, i), None)


class FakeVectorStore:
    def __init__(self): self.ids = set()
    def upsert(self, t, ids, texts, vectors): self.ids.update(ids)
    def search(self, t, v, k): return []
    def delete(self, t, i): self.ids.discard(i)


class FakeEmbedder:
    dim = 3
    def embed(self, texts): return [[0.0, 0.0, 0.0] for _ in texts]


CHUNKS = ["meo thich ngu", "cho thich chay", "chim thich bay"]


def snapshot(label, manifest, bm25, docs, vec):
    print(f"    manifest  : {manifest}")
    print(f"    BM25 docs : {sorted(bm25.doc_len.get('t1', {}))}  (doc_count={bm25.doc_count.get('t1', 0)})")
    print(f"    DocStore  : {sorted(k[1] for k in docs.data)}")
    print(f"    Qdrant    : {sorted(vec.ids)}")


def run(label, manifest, bm25, docs, vec):
    print(f"\n>>> {label}")
    input("    (dự đoán upserted/skipped/deleted rồi bấm Enter) ")
    result = ingest_document("t1", "doc_A", CHUNKS, manifest, bm25, vec, docs, FakeEmbedder())
    print(f"    KẾT QUẢ   : {result}")
    snapshot(label, manifest, bm25, docs, vec)


# ---------- một đời server ----------
manifest, bm25, docs, vec = {}, BM25Index(), FakeDocStore(), FakeVectorStore()

run("KỊCH BẢN 0 — ingest lần đầu", manifest, bm25, docs, vec)
run("KỊCH BẢN 1 — ingest lại y hệt, KHÔNG restart", manifest, bm25, docs, vec)

print("\n### Có người xoá tay 3 chunk khỏi BM25 (manifest KHÔNG đụng tới)")
bm25.index.pop("t1", None); bm25.doc_len.pop("t1", None); bm25.doc_count.pop("t1", None)
snapshot("sau khi xoá tay", manifest, bm25, docs, vec)
run("KỊCH BẢN 2 — ingest lại y hệt sau khi kho BM25 bị rỗng", manifest, bm25, docs, vec)

# ---------- restart: manifest RAM chết cùng tiến trình ----------
print("\n### RESTART (bản đã fix #25: manifest là dict RAM → chết cùng 3 kho)")
manifest, bm25, docs, vec = {}, BM25Index(), FakeDocStore(), FakeVectorStore()
run("KỊCH BẢN 4 — ingest lại y hệt sau restart", manifest, bm25, docs, vec)

# ---------- restart kiểu CŨ: manifest sống trên đĩa, 3 kho RAM ----------
print("\n### RESTART kiểu CŨ (bug #25: manifest bền hơn 3 kho)")
manifest_cu = {"t1": {"doc_A": {"0": __import__("hashlib").sha256(CHUNKS[0].encode()).hexdigest(),
                               "1": __import__("hashlib").sha256(CHUNKS[1].encode()).hexdigest(),
                               "2": __import__("hashlib").sha256(CHUNKS[2].encode()).hexdigest()}}}
bm25, docs, vec = BM25Index(), FakeDocStore(), FakeVectorStore()
run("KỊCH BẢN 5 — manifest sống sót, 3 kho rỗng", manifest_cu, bm25, docs, vec)
