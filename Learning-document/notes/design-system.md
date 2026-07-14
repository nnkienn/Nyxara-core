# 🏛️ Design System — quyết định kiến trúc

> Nơi ghi **vì sao code được tổ chức như hiện tại**. Mỗi mục = 1 quyết định, kèm lý do
> và hệ quả. Đọc file này là hiểu được "luật chơi" của repo mà không phải dò khắp code.

**Cách thêm mục:** copy template dưới, điền. Ngày tuyệt đối (2026-07-13), không "hôm nay".

```
### <Tên quyết định>  ·  <ngày>
- **Quyết định:** …
- **Vì sao:** …
- **Hệ quả / ràng buộc:** … (cái gì giờ BẮT BUỘC hoặc BỊ CẤM vì quyết định này)
- **Liên quan:** [[glossary#term]] · file/port nào
```

---

## Nền tảng (chốt từ đầu)

### Kiến trúc Hexagonal (Ports & Adapters)  ·  2026-07-13
- **Quyết định:** `domain` (thực thể + port thuần) ← `application` (use case) ← `infrastructure`
  (adapter) ← `presentation` (FastAPI). Chiều phụ thuộc chỉ hướng **vào trong**.
- **Vì sao:** thay Qdrant / LLM engine / web framework mà không đụng logic nghiệp vụ; test
  use case bằng fake adapter, không cần dịch vụ thật.
- **Hệ quả:** `domain` **cấm** import framework (fastapi, qdrant_client…). Adapter *implements*
  port, không được gọi ngược lên application.

### Ranh giới Core ↔ Cloud  ·  2026-07-13
- **Quyết định:** repo này (`nyxara-core`, MIT) là **bộ não AI thuần**; billing/auth/metering
  ở repo riêng (`nyxara-cloud`). `tenant_id` = **namespace**, KHÔNG phải customer.
- **Vì sao:** core sạch để học + fork; đổi mô hình kinh doanh không đụng bộ não.
- **Hệ quả:** CI **cấm** `import stripe` / auth / billing trong core. Core phơi Port
  (`MeteringPort`, `EntitlementPort`), cloud cắm Adapter. Xem roadmap §Ranh giới Core↔Cloud.

### Reset 2026-07-13 — build lại từ đầu
- **Quyết định:** xóa toàn bộ harvester + bộ não RAG cũ (kể cả 74 test đã xanh), giữ Docker +
  khung hexagonal rỗng. Code lại từ Phase 0 theo phương pháp 6 bước.
- **Vì sao:** code cũ phần lớn do AI sinh, không tự hiểu hết → mâu thuẫn triết lý "hiểu để soi".
  Bắt đầu lại để mỗi dòng đều tự tay + tự hiểu.
- **Hệ quả:** roadmap reset mọi ✅ về ⏳. Code cũ vẫn nằm trong git history (commit `817d2d1`)
  nếu cần tham khảo — nhưng KHÔNG copy-paste lại; gõ tay từng phần.

### Quy ước đặt tên  ·  2026-07-13
- **Quyết định:** repo `nyxara-core` / cloud `nyxara-cloud`. Bỏ hết tên cũ `n-assistant` / `nassistant`.
- **Hệ quả:** service Docker, image, container đều prefix `nyxara-core-*`.

---

## (Thêm các quyết định mới bên dưới khi build từng phase)
