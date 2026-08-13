import hashlib
import json
import os

from app.application.retrieval.bm25_index import BM25Index
from app.domain.ports.doc_store import DocStore
from app.domain.ports.embedder import Embedder
from app.domain.ports.vector_store import VectorStore


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def load_seen(path: str) -> set[str]:
    if not os.path.exists(path):
        return set()
    with open(path) as f:
        return set(json.load(f))
def load_manifest(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)


def save_manifest(path: str, manifest: dict) -> None:
    with open(path, "w") as f:
        json.dump(manifest, f)


def get_doc_manifest(manifest: dict, tenant_id: str, doc_id: str) -> dict[str, str]:
    # TODO: đi xuống đúng 2 tầng (tenant_id rồi doc_id) trong `manifest`, trả về
    # {chunk_index: hash} nếu đã từng ingest doc này, hoặc {} nếu tenant/doc chưa
    # từng xuất hiện (giống cách bạn đã guard "if tenant_id in ... and doc_id in ..."
    # ở BM25Index.remove_document / InMemoryDocStore.delete — nhưng đây là ĐỌC, dùng
    # .get() lồng nhau thay vì if, tránh KeyError khi tenant/doc chưa tồn tại).
    return manifest.get(tenant_id, {}).get(doc_id, {})

def diff_manifest(
    old_manifest: dict[str, str], new_manifest: dict[str, str]
) -> tuple[list[str], list[str], list[str]]:
    to_upsert: list[str] = []
    to_skip: list[str] = []
    to_delete: list[str] = []

    all_indices = set(old_manifest) | set(new_manifest)

    for chunk_index in all_indices:
        if chunk_index not in new_manifest:
            to_delete.append(chunk_index)
        elif chunk_index not in old_manifest:
            to_upsert.append(chunk_index)
        elif old_manifest[chunk_index] != new_manifest[chunk_index]:
            to_upsert.append(chunk_index)
        else:
            to_skip.append(chunk_index)
    return to_upsert, to_skip, to_delete


def save_seen(path: str, seen: set[str]) -> None:
    with open(path, "w") as f:
        json.dump(list(seen), f)


def incremental_ingest(chunks: list[str], seen_path: str) -> list[str]:
    seen = load_seen(seen_path)
    new_chunks = []

    for chunk in chunks:
        h = _hash(chunk)
        if h in seen:
            continue
        new_chunks.append(chunk)
        seen.add(h)
        save_seen(seen_path, seen)
    return new_chunks

def ingest_document(
    tenant_id: str,
    doc_id: str,
    chunks: list[str],
    manifest_path: str,
    bm25_index: BM25Index,
    vector_store: VectorStore,
    doc_store: DocStore,
    embedder: Embedder,
) -> None:
    manifest = load_manifest(manifest_path)
    old_doc = get_doc_manifest(manifest, tenant_id, doc_id)
    new_doc = {str(i): _hash(chunk) for i, chunk in enumerate(chunks)}
    to_upsert, to_skip, to_delete = diff_manifest(old_doc, new_doc)
    to_upsert_chunks = [chunks[int(i)] for i in to_upsert]

    for chunk_index in to_delete:
        chunk_id = f"{doc_id}:{chunk_index}"
        bm25_index.remove_document(tenant_id, chunk_id)
        vector_store.delete(tenant_id, chunk_id)
        doc_store.delete(tenant_id, chunk_id)


    to_upsert_ids = [f"{doc_id}:{i}" for i in to_upsert]
    for chunk_id, text in zip(to_upsert_ids, to_upsert_chunks):
        doc_store.save(tenant_id, chunk_id, text)
        bm25_index.add_document(tenant_id, chunk_id, text)

    if to_upsert_ids:
        vectors = embedder.embed(to_upsert_chunks)
        vector_store.upsert(tenant_id, to_upsert_ids, to_upsert_chunks, vectors)

    manifest.setdefault(tenant_id, {})[doc_id] = new_doc
    save_manifest(manifest_path, manifest)
    