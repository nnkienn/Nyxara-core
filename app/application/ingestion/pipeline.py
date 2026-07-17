import hashlib
import json
import os


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def load_seen(path: str) -> set[str]:
    if not os.path.exists(path):
        return set()
    with open(path) as f:
        return set(json.load(f))


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
