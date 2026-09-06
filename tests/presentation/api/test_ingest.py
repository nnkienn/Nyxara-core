"""Integration test cho POST /ingest — đi xuyên handler, không gọi thẳng ingest_document.

Lý do tồn tại: test unit ở tầng pipeline KHÔNG đi qua dòng dựng IngestResponse,
nên nó xanh kể cả khi handler báo cáo sai. Test này đi qua dòng đó.
"""

from fastapi.testclient import TestClient

from app.main import app


def test_ingest_lan_2_bao_cao_trung_thuc(monkeypatch):
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")

    payload = {
        "tenant_id": "t1",
        "doc_id": "d1",
        "text": "con mèo đen",
    }

    with TestClient(app) as client:
        lan_1 = client.post("/ingest", json=payload).json()
        lan_2 = client.post("/ingest", json=payload).json()

    # TODO A — lần 1 là lần đầu tiên doc này vào kho. 4 con số phải là gì?
    assert lan_1 == {"chunk_count": 1, "chunk_upserted": 1, "chunk_skipped": 0, "chunk_deleted": 0}

    # TODO B — lần 2 gửi Y HỆT lần 1. 4 con số phải là gì?
    #   Đây mới là dòng bắt bug: nếu ai đó quay lại bịa 3 con số trong handler,
    #   dòng này phải ĐỎ.
    assert lan_2 == {"chunk_count": 1, "chunk_upserted": 0, "chunk_skipped": 1, "chunk_deleted": 0}


def test_restart_thi_quen_sach_khong_skip_oan(monkeypatch):
    """Bug #25 — sau restart, 3 kho rỗng thật, nên manifest KHÔNG được nói 'đã có rồi'.

    Hai khối `with` NGANG HÀNG (không lồng nhau) = hai đời tiến trình:
    khối 1 đóng lại -> lifespan kết thúc; khối 2 mở ra -> lifespan chạy lại từ đầu,
    dựng BM25Index / QdrantStore / InMemoryDocStore / manifest mới tinh.
    """
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")

    payload = {
        "tenant_id": "t1",
        "doc_id": "d1",
        "text": "con mèo đen",
    }

    with TestClient(app) as client:
        lan_1 = client.post("/ingest", json=payload).json()

    with TestClient(app) as client:
        lan_2 = client.post("/ingest", json=payload).json()

    assert lan_1 == {"chunk_count": 1, "chunk_upserted": 1, "chunk_skipped": 0, "chunk_deleted": 0}

    # sau restart kho rỗng -> phải ghi LẠI, không được skip oan
    assert lan_2 == {"chunk_count": 1, "chunk_upserted": 1, "chunk_skipped": 0, "chunk_deleted": 0}
