"""POST /ask — endpoint chạy CRAG pipeline cho 1 câu hỏi.

Graph được dựng SẴN 1 lần lúc startup (composition root trong main.py) và cất ở
app.state.crag_graph. Route chỉ lấy ra và invoke — KHÔNG dựng lại mỗi request.
"""

from __future__ import annotations

from fastapi import APIRouter, Request

from app.presentation.api.schemas.crag import AskRequest, AskResponse, Hit

router = APIRouter(tags=["crag"])


@router.post("/ask", response_model=AskResponse)
async def ask(body: AskRequest, request: Request) -> AskResponse:
    graph = request.app.state.crag_graph

    # Dựng tờ giấy state ban đầu. Khởi tạo sẵn các ô trung gian —
    # đặc biệt attempts=0, tránh KeyError ở "đường thành công" (correct_node
    # không chạy → attempts chưa từng được ghi).
    initial_state = {
        "query": body.query,
        "tenant_id": body.tenant_id,
        "top_k": body.top_k,
        "attempts": 0,
    }

    # ainvoke (async) vì grade_node gọi LLM là async — "async lây" lên tới đây.
    final_state = await graph.ainvoke(initial_state)

    # Đổi RetrievalHit (domain) → Hit (pydantic, hợp đồng API).
    context = [
        Hit(doc_id=h.doc_id, text=h.text, score=h.score, source=h.source)
        for h in final_state["context"]
    ]

    return AskResponse(
        query=body.query,
        verdict=final_state["verdict"],
        attempts=final_state.get("attempts", 0),
        context=context,
    )
