"""Request / Response schema cho endpoint CRAG (/ask).

Pydantic model = "hợp đồng" dữ liệu vào/ra API. FastAPI dùng nó để:
  - validate input (thiếu field / sai kiểu → tự trả 422, không cần check tay)
  - sinh docs tự động ở /docs
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """Body của POST /ask — câu hỏi của khách."""

    query: str = Field(..., description="Câu hỏi của người dùng")
    tenant_id: str = Field(..., description="Namespace của kênh — mọi search lọc theo nó")
    top_k: int = Field(5, ge=1, le=20, description="Số chunk sạch muốn lấy cuối cùng")


class Hit(BaseModel):
    """1 chunk trong kết quả trả về."""

    doc_id: str
    text: str
    score: float
    source: str


class AskResponse(BaseModel):
    """Kết quả CRAG trả cho client."""

    query: str
    verdict: str          # CORRECT | AMBIGUOUS | INCORRECT
    attempts: int         # số lần CRAG đã tìm lại
    context: list[Hit]    # bundle chunk sạch cuối cùng
