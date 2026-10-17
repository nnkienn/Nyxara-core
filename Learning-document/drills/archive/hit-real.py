# Drill 08/10 tối — chạy hit_at_k CỦA BẠN (trong hit-at-k.py) trên đề thật Zalo Legal.
# Claude nối dây: đọc 61K điều + 788 câu test, BM25 khoanh top-10 mỗi câu, lưu cache.
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "zalo_legal"
CACHE = DATA / "bm25_top10_test.json"


def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def build_results() -> tuple[list[list[str]], list[str]]:
    if CACHE.exists():
        saved = json.loads(CACHE.read_text())
        return saved["results"], saved["answers"]

    # BM25 tối giản (k1=1.5, b=0.75) bằng chỉ mục ngược, title + text
    doc_ids, doc_lens, postings = [], [], defaultdict(list)
    for line in open(DATA / "corpus.jsonl"):
        doc = json.loads(line)
        tokens = tokenize(doc["title"] + " " + doc["text"])
        index = len(doc_ids)
        doc_ids.append(doc["_id"])
        doc_lens.append(len(tokens))
        for term, tf in Counter(tokens).items():
            postings[term].append((index, tf))
    n_docs, avg_len = len(doc_ids), sum(doc_lens) / len(doc_lens)

    queries = {}
    for line in open(DATA / "queries.jsonl"):
        q = json.loads(line)
        queries[q["_id"]] = q["text"]
    correct = {}
    for line in open(DATA / "qrels" / "test.jsonl"):
        r = json.loads(line)
        correct.setdefault(r["query-id"], r["corpus-id"])   # câu có nhiều điều đúng: lấy điều đầu

    results, answers = [], []
    for query_id, answer in correct.items():
        scores = defaultdict(float)
        for term in set(tokenize(queries[query_id])):
            plist = postings.get(term, [])
            idf = math.log(1 + (n_docs - len(plist) + 0.5) / (len(plist) + 0.5))
            for index, tf in plist:
                norm = tf + 1.5 * (1 - 0.75 + 0.75 * doc_lens[index] / avg_len)
                scores[index] += idf * tf * 2.5 / norm
        top10 = sorted(scores, key=scores.get, reverse=True)[:10]
        results.append([doc_ids[index] for index in top10])
        answers.append(answer)

    CACHE.write_text(json.dumps({"results": results, "answers": answers}, ensure_ascii=False))
    return results, answers


# 09/10: dùng bản trong app/ (bạn gõ lại, 5 test xanh)
import sys
sys.path.insert(0, str(ROOT))
from app.evaluation.metrics import hit_at_k

results, answers = build_results()
print(f"\nĐề thật: {len(results)} câu · mỗi câu máy khoanh {len(results[0])} điều")
print("Câu 0 — máy khoanh 3 điều đầu:", results[0][:3], "| đáp án:", answers[0])

# ===== BẠN GÕ Ở ĐÂY: in Hit@k của cả đề với k = 1, 3, 5, 10 (mỗi k một dòng) =====
for x in [1,3,5,10]:
    print("=Hit@" , x , "->" , hit_at_k(results, answers, x))
# ===== HẾT CHỖ GÕ =====
