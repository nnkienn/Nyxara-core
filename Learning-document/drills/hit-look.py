# Drill 09/10 tối — soi MỘT câu thật: câu hỏi · đáp án · 10 điều máy khoanh.
# Bạn chỉ đổi số i bên dưới (0 tới 787) rồi chạy lại.
import json
from pathlib import Path

i = 42   # ← ĐỔI SỐ NÀY

DATA = Path(__file__).resolve().parents[2] / "data" / "zalo_legal"
saved = json.loads((DATA / "bm25_top10_test.json").read_text())
results, answers = saved["results"], saved["answers"]

query_ids = []
for line in open(DATA / "qrels" / "test.jsonl"):
    query_id = json.loads(line)["query-id"]
    if query_id not in query_ids:
        query_ids.append(query_id)
questions = {}
for line in open(DATA / "queries.jsonl"):
    q = json.loads(line)
    questions[q["_id"]] = q["text"]
titles = {}
wanted = set(results[i]) | {answers[i]}
for line in open(DATA / "corpus.jsonl"):
    doc = json.loads(line)
    if doc["_id"] in wanted:
        titles[doc["_id"]] = doc["title"][:90]

print(f"CÂU {i}: {questions[query_ids[i]]}")
print(f"ĐÁP ÁN (qrels): {answers[i]} — {titles[answers[i]]}\n")
print("MÁY KHOANH (results[i]):")
for row, doc_id in enumerate(results[i], start=1):
    mark = "   ← ĐÁP ÁN" if doc_id == answers[i] else ""
    print(f"  dòng {row:2}: {doc_id:22} {titles[doc_id]}{mark}")
