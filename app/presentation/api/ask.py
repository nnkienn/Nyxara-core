"""POST /ask — CRAG query endpoint."""

from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()


class AskRequest(BaseModel):
    tenant_id: str
    query: str


class AskResponse(BaseModel):
    answer: str


@router.post("/ask", response_model=AskResponse, tags=["ask"])
def ask(payload: AskRequest, request: Request) -> AskResponse:
    # `def` thường, KHÔNG `async def` — graph.invoke() gọi httpx.post đồng bộ tới Ollama
    # (chặn luồng); FastAPI tự chạy handler sync trong threadpool riêng, không chặn event loop.
    graph = request.app.state.graph
    result = graph.invoke(
        {
            "query": payload.query,
            "tenant_id": payload.tenant_id,
            "attempts": 0,
        }
    )
    return AskResponse(answer=result["answer"])
