# QdrantClient: "sợi dây kết nối" tới Qdrant, dùng để gọi mọi lệnh (tạo kho, lưu, tìm...).
# Distance/VectorParams: cấu hình khi TẠO kho (loại thước đo + kích thước vector).
# PointStruct: khuôn dữ liệu cho 1 điểm lưu vào kho (id + vector + payload).
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct

from qdrant_client.models import Filter, FieldCondition, MatchValue
from app.domain.ports.vector_store import SearchHit

class QdrantStore:
    def __init__(self, client: QdrantClient, collection: str, dim: int):
        self.client = client
        self.collection = collection
        self._ensure_collection(dim)

    def _ensure_collection(self, dim):
        # "ensure" = ĐẢM BẢO có, không phải LUÔN LUÔN tạo mới.
        # Nếu kho đã tồn tại mà cứ create_collection() lại -> Qdrant báo lỗi 409 (đã gặp).
        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )

    def upsert(self, tenant_id: str, ids: list[str], texts: list[str], vectors: list[list[float]]) -> None:
        # zip khoá 3 danh sách song song lại, duyệt cùng lúc theo từng vị trí:
        # (ids[0], texts[0], vectors[0]), rồi (ids[1], texts[1], vectors[1])...
        # payload = dữ liệu "đính kèm" mỗi vector, để sau này biết nó thuộc tenant nào + text gốc.
        # uuid5(NAMESPACE, id) -> UUID cố định từ chuỗi id gốc: cùng id luôn ra cùng UUID
        # (Qdrant chỉ chấp nhận id dạng số nguyên hoặc UUID, không nhận string tuỳ ý)
        # + ingest lại cùng id -> ghi đè đúng điểm cũ, không tạo bản trùng (idempotent).
        points = [
            PointStruct(
                id=str(uuid.uuid5(uuid.NAMESPACE_DNS, id)),
                vector=vector,
                payload={"tenant_id": tenant_id, "text": text},
            )
            for id, text, vector in zip(ids, texts, vectors)
        ]
        self.client.upsert(
            collection_name=self.collection,
            points=points,
        )


    def search(self, tenant_id : str , query_vector: list[float], top_k: int)->list[SearchHit]:
        filter = Filter(
            must = [
                FieldCondition(
                    key= "tenant_id",
                    match = MatchValue(value=tenant_id)
                )
            ]
        )
        res = self.client.query_points(          # search -> query_points
            collection_name=self.collection,
            query=query_vector,                  # query_vector= -> query=
            query_filter=filter,
            limit=top_k,
        ).points                                 # thêm .points ở cuối (response mới bọc trong .points)

        return [
            SearchHit(id=hit.id, text=hit.payload["text"], score=hit.score)
            for hit in res
        ]
        