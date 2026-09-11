# Ôn +7 CRAG — code tay lại PHÍA GHI của fix bug #26, ĐÓNG SÁCH (2026-09-11)
# - Đóng hết tab app/application/generation/*. Không mở git log, không mở bug-log.
# - Hộp 20'. Hết giờ thì dừng, viết tới đâu báo tới đó.
# - Viết xong báo Claude — Claude cắm 2 phần dưới đây vào graph thật và chạy test thật.

from typing import TypedDict

from app.application.generation.decision import decide
from app.domain.ports.grader import grader

# Phần 1 — schema state của graph (bản thật nằm ở state.py)
class CRAGeneratorState(TypedDict):
    query : str
    retrieved_docs : list[str]
    verdict : str
    attempts :  int
    answer : str
    tenant_id  : str
    grades : list[bool]
    candidate_k : int


# Phần 2 — node chấm điểm (bản thật nằm ở node.py)
def make_grade_node(grader, correct_threshold=0.6, incorrect_threshold=0.0):
    def grade_node(state : CRAGeneratorState) :
        query = state["query"]
        docs = state["retrieved_docs"]
        grades = grader.grade(query, docs)
        verdict = decide(grades, correct_threshold, incorrect_threshold)
        print("CHẤM:", grades, verdict)      ← dòng tạm để NHÌN THẤY kết quả, 2d sẽ xoá
    return grade_node
