# SÁNG 22/09 — BÀI ĐO Cặp 17: ô của "match" điền gì
# Bạn KHÔNG gõ gì trong file này. Chỉ chạy rồi đọc số.
# Chạy: .venv/bin/python Learning-document/drills/2026-09-22-sang-do-cap17.py

from qdrant_client import QdrantClient, models

KHO = [
    (1, {"co_quan": "Quoc hoi",   "loai": "Luat",       "nam": 2015}),
    (2, {"co_quan": "Chinh phu",  "loai": "Nghi dinh",  "nam": 2018}),
    (3, {"co_quan": "Bo Tai chinh", "loai": "Thong tu", "nam": 2021}),
]

client = QdrantClient(":memory:")
client.create_collection(
    collection_name="vb",
    vectors_config=models.VectorParams(size=2, distance=models.Distance.COSINE),
)
client.upsert(
    collection_name="vb",
    points=[models.PointStruct(id=i, vector=[0.1, 0.9], payload=p) for i, p in KHO],
)


def thu(ten_o: str) -> None:
    """Dung to don loc co_quan == 'Quoc hoi', o khoa cua match dien `ten_o`."""
    print(f'--- to don: {{"key": "co_quan", "match": {{"{ten_o}": "Quoc hoi"}}}}')
    try:
        dieu_kien = models.FieldCondition(
            key="co_quan",
            match=models.MatchValue(**{ten_o: "Quoc hoi"}),
        )
    except Exception as e:
        print(f"    NO ngay luc DUNG to don: {type(e).__name__}")
        print(f"    {str(e).splitlines()[1].strip()} | {str(e).splitlines()[2].strip()}")
        print()
        return

    ra = client.query_points(
        collection_name="vb",
        query=[0.1, 0.9],
        query_filter=models.Filter(must=[dieu_kien]),
        limit=10,
    ).points
    print(f"    chay duoc -> song {len(ra)} van ban: {[p.payload['co_quan'] for p in ra]}")
    print()


thu("eq")
thu("value")


# ─── VONG 2 (22/09): eq tren SO, khong phai chuoi ────────────────
# Cung cau hoi, chi doi gia tri tu chuoi sang so.

def thu_so(ten_o: str) -> None:
    print(f'--- to don: {{"key": "nam", "match": {{"{ten_o}": 2015}}}}')
    try:
        dieu_kien = models.FieldCondition(
            key="nam",
            match=models.MatchValue(**{ten_o: 2015}),
        )
    except Exception as e:
        print(f"    NO ngay luc DUNG to don: {type(e).__name__}")
        print(f"    {str(e).splitlines()[1].strip()} | {str(e).splitlines()[2].strip()}")
        print()
        return

    ra = client.query_points(
        collection_name="vb",
        query=[0.1, 0.9],
        query_filter=models.Filter(must=[dieu_kien]),
        limit=10,
    ).points
    print(f"    chay duoc -> song {len(ra)} van ban: {[p.payload['nam'] for p in ra]}")
    print()


print("===== VONG 2: eq tren SO =====")
thu_so("eq")
thu_so("value")
