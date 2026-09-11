# Máy chấm cho drills/2026-09-11-crag-phia-ghi.py — CLAUDE chạy, user chỉ đọc số
# (luật 09/09: bài đo do Claude dựng thì Claude chạy hộ).
#
#   PYTHONPATH=. .venv/bin/python Learning-document/drills/2026-09-11-crag-cham.py
#
# Cắm bài của user vào graph THẬT (build_graph + retrieve/generate thật trong app/):
# - luôn thay schema bằng CRAGeneratorState của user
# - thay make_grade_node của user nếu Phần 2 đã viết (còn `...` thì giữ bản thật)
# Rồi chạy 3 kiểu grader, in nhật ký candidate_k mà retriever nhận được.

import importlib.util

spec = importlib.util.spec_from_file_location("bai", "Learning-document/drills/2026-09-11-crag-phia-ghi.py")
bai = importlib.util.module_from_spec(spec)
# Python 3.9 (máy Mac): LangGraph đọc kiểu của TypedDict qua sys.modules[tên module] → phải đăng ký, không thì KeyError: 'bai'
import sys
sys.modules["bai"] = bai
spec.loader.exec_module(bai)

import app.application.generation.graph as g
from app.application.generation.state import CRAGeneratorState as SchemaThat

g.CRAGeneratorState = bai.CRAGeneratorState
phan2_da_viet = callable(bai.make_grade_node(object()))
if phan2_da_viet:
    g.make_grade_node = bai.make_grade_node

cua_ban = bai.CRAGeneratorState.__annotations__
that = SchemaThat.__annotations__
print("PHẦN 1 — schema so với state.py thật:")
for k in that:
    print(f"  {k:15} thật={that[k]!s:16} bạn={cua_ban.get(k, '(THIẾU)')!s}")
for k in cua_ban:
    if k not in that:
        print(f"  {k:15} (key LẠ — bản thật không có)")
print("\nPHẦN 2 — make_grade_node:", "dùng BÀI CỦA BẠN" if phan2_da_viet else "chưa viết, đang dùng bản thật")


class Retriever:
    def __init__(self):
        self.log = []

    def search(self, tenant_id, query, candidate_k, top_k):
        self.log.append(candidate_k)
        return [("a", 1), ("b", 1), ("c", 1)]


class DocStore:
    def get(self, tenant_id, doc_id):
        return "doc " + doc_id


class Grader:
    def __init__(self, grades):
        self.grades = grades

    def grade(self, query, docs):
        return self.grades


class Generator:
    def generate(self, query, docs):
        return "tra loi"


for ten, grades, mong in [
    ("chê hết   [F,F,F]", [False] * 3, [10, 20, 40]),
    ("khen hết  [T,T,T]", [True] * 3, [10]),
    ("lẫn lộn   [T,F,F]", [True, False, False], [10]),
]:
    r = Retriever()
    try:
        kq = g.build_graph(r, DocStore(), Grader(grades), Generator(), candidate_k=10, max_attempts=3).invoke(
            {"tenant_id": "t1", "query": "q", "attempts": 0}
        )
        ket_luan = "XANH" if r.log == mong else "ĐỎ"
        print(f"\nGrader {ten}: nhật ký candidate_k = {r.log}  (phải là {mong})  -> {ket_luan}"
              f"   verdict={kq.get('verdict')}  attempts cuối={kq.get('attempts')}")
    except Exception as e:
        print(f"\nGrader {ten}: NỔ {type(e).__name__} — {str(e).splitlines()[0]}   (nhật ký tới lúc nổ: {r.log})")
