# Quiz Card — Tự kiểm tra
> Đọc câu hỏi → tự trả lời → lật xem đáp án.
> Giải thích sâu → xem notes-knowledge.md.

---

## Phase 2 — Ingest Pipeline

**Q: `bge-m3` output vector có dimension bao nhiêu?**
A: 1024 chiều.

**Q: Tại sao phải L2-normalize vector sau khi embed?**
A: Qdrant tính cosine bằng dot product — chỉ đúng khi `‖v‖ = 1`. Normalize → unit vector → cosine = dot product.

**Q: UUID5 giải quyết vấn đề gì trong ingestion?**
A: Idempotent upsert — cùng chunk ingest 2 lần → cùng UUID → Qdrant overwrite, không duplicate. UUID4 → random ID → duplicate records.

**Q: UUID5 ghép `text + tenant_id` thay vì chỉ `text` — tại sao?**
A: Cùng text có thể tồn tại ở 2 tenant. Chỉ dùng `text` → cùng UUID → tenant B ghi đè data tenant A.

**Q: `ensure_collection(dim=512)` nhưng vector 1024 chiều — chuyện gì xảy ra?**
A: Qdrant throw error ngay (hard error). Không phải "mất thông tin", mà crash hoàn toàn.

**Q: Tại sao `search()` nhận 1 vector, còn `embed()` nhận batch?**
A: `embed()` ingest nhiều chunk cùng lúc. `search()` chỉ có 1 query tại 1 thời điểm.

**Q: Tại sao `upsert()` trả `int` thay vì `None`?**
A: Caller biết đã lưu bao nhiêu chunk. `None` → không debug được khi ingest 0 chunk.

**Q: Filter `tenant_id` trong Qdrant chạy trước hay sau cosine?**
A: Trước (pre-filtering). Lọc tenant → chỉ tính cosine trên tập đã lọc → nhanh hơn.

**Q: `if not texts: return 0` guard tránh lỗi gì?**
A: `embed([])` → `vectors = []` → `vectors[0]` → **IndexError**. Guard tránh crash.

**Q: `dim=len(vectors[0])` thay vì hardcode `1024` — lợi ích gì?**
A: Đổi model sang dim khác → không cần sửa IngestionService.

**Q: Nominal typing vs Structural typing là gì?**
A: Nominal = match theo tên/kế thừa. Structural = match theo cấu trúc (có method gì). Python Protocol dùng structural — có đúng method là hợp lệ, không cần kế thừa.

**Q: `use_fp16=True` trong BGEEmbedder có tác dụng gì?**
A: Float16 thay float32 → nửa RAM, nhanh ~2×. Độ chính xác embedding gần như không đổi.

---

## Phase 3 — Search Pipeline

**Q: Tại sao `_docs: list = []` trong dataclass là trap? Fix thế nào?**
A: Mọi instance share cùng 1 list. Fix: `_docs: list = field(default_factory=list)`.

**Q: `add()` tokenize `text.lower().split()`. `search()` không `.lower()` → chuyện gì?**
A: Token "KEM" ≠ "kem" → tf=0 → BM25 score=0 → không tìm được gì dù data đầy đủ.

**Q: `if not tenant_docs: return []` tránh lỗi gì?**
A: `sum(...) / len(tenant_docs)` → ZeroDivisionError nếu rỗng.

**Q: TF đo gì? IDF đo gì? Tại sao nhân TF × IDF?**
A: TF = từ xuất hiện bao nhiêu lần trong doc này. IDF = độ HIẾM của từ trong toàn corpus. TF × IDF → doc chứa nhiều lần từ hiếm → thật sự liên quan.

---

**Q: RRF nhận `list[list[str]]` thay vì 2 param riêng — lợi ích?**
A: Thêm nguồn thứ 3 không cần sửa signature, chỉ thêm 1 phần tử vào list.

**Q: `scores.get(doc_id, 0.0)` thay vì `scores[doc_id]` — tại sao?**
A: Lần đầu gặp doc mới → `scores[doc_id]` KeyError. `.get` trả default 0.0.

**Q: Doc rank 1 ở cả dense lẫn BM25 vs doc rank 1 chỉ dense — ai thắng RRF?**
A: Doc xuất hiện cả 2 nguồn: `2/61 ≈ 0.033`. Doc chỉ 1 nguồn: `1/61 ≈ 0.016`. Doc 2 nguồn thắng gấp đôi.

**Q: Tại sao không cộng score BM25 + cosine trực tiếp?**
A: BM25 range `[0,∞)`, cosine range `[0,1]` — khác đơn vị, không cộng có nghĩa. RRF dùng rank → scale-invariant.

## Phase 4 — Generation (CRAG)
*(sẽ cập nhật khi học)*
