# 🃏 Thẻ phân biệt — các cặp dễ lẫn

> **Vì sao có file này (tạo 2026-09-03):** ôn +1 ngày sau khi qua cổng đóng-sách Trạm 1 & 2, sai
> 3/4 câu. Cả 4 lỗi cùng **một loại**: không phải quên mất kiến thức, mà là **lẫn 2 thứ na ná
> nhau**. Loại lỗi này không chữa bằng giải thích thêm (đã giải thích hôm trước, 12 tiếng sau vẫn
> lẫn) — chữa bằng **drill phân biệt**: bị ép chọn giữa 2 phương án dễ lẫn, lặp nhiều lượt, phản
> hồi nhanh. Cùng cơ chế với drill cú pháp Python đã hiệu quả 2 lần (28/08, 01/09).
>
> **Cách dùng:** đọc 5 phút trước mỗi buổi ôn. Câu hỏi drill lấy từ cột "Câu hỏi phân biệt".
> Thêm cặp mới mỗi khi phát hiện một chỗ lẫn thật trong lúc trace.

---

## Cặp 1 — `to_upsert` vs `to_delete`  (Trạm 1)

**Câu hỏi phân biệt duy nhất:** *chỉ số (index) đó CÒN trong `new_doc` không?*

| | `to_upsert` | `to_delete` |
|---|---|---|
| Điều kiện | index **CÒN** trong `new_doc` | index **KHÔNG CÒN** trong `new_doc` |
| Dòng code | `elif chunk_index not in old_manifest` (mới)<br>`elif old[i] != new[i]` (đổi nội dung) | `if chunk_index not in new_manifest` |
| Tình huống đời thật | sửa 1 câu trong doc; thêm đoạn mới | doc bị **cắt ngắn** → chunk cuối biến mất |
| Ví dụ | `["A","B"]` → `["A","B_sửa"]` → `to_upsert=["1"]` | `["A","B","C"]` → `["A","B"]` → `to_delete=["2"]` |

> ⚠️ **Bẫy đã mắc 4 lần:** "thay thế / đổi nội dung" → **`to_upsert`**, KHÔNG phải `to_delete`.
> Đổi nội dung thì index vẫn còn nguyên chỗ cũ, chỉ hash khác. `to_delete` chỉ dành cho thứ
> **biến mất hẳn**.
>
> Câu thần chú: **đổi = upsert · mất = delete**

---

## Cặp 2 — lưu **hash** vs lưu **danh sách index**  (Trạm 1)

| Nếu manifest lưu... | Bắt được | BỎ SÓT |
|---|---|---|
| chỉ danh sách index `["0","1","2"]` | thêm chunk · bớt chunk | ❌ **sửa nội dung tại chỗ** |
| index → hash `{"0": h_A, ...}` | thêm · bớt · **sửa tại chỗ** | — |

**Tình huống bị bỏ sót có tên cụ thể:** `"chó"` → `"vịt"`, **cùng index `"1"`**. Index không đổi
→ so index thì tưởng không có gì → bản mới không bao giờ được ghi vào 3 kho. Hash bắt được vì
vân tay nội dung đổi.

---

## Cặp 3 — cái nào là **model AI**, cái nào **không**  (Trạm 2)

| Thành phần | Model AI? | Thực chất nó là gì |
|---|---|---|
| **Bi-encoder** (`BGEEmbedder`) | ✅ **CÓ** | mạng nơ-ron: text → vector |
| **BM25** (`BM25Index`) | ❌ **KHÔNG** | **đếm chữ**: TF × IDF ÷ length norm. Toàn số học, không có trọng số học được. **Bạn đã tự viết tay nó ở Phase 2.1** |
| **RRF** (`reciprocal_rank_fusion`) | ❌ **KHÔNG** | **toán thuần**: cộng `1/(k+rank)`. ~10 dòng |
| **Cross-encoder** (`BGEReranker`) | ✅ **CÓ** | mạng nơ-ron, **đắt nhất pipeline** |

> Mẹo nhớ: **2 thằng "encoder" là model. 2 thằng còn lại (BM25, RRF) là số học viết tay được.**

---

## Cặp 4 — **Bi-encoder** vs **Cross-encoder**  (Trạm 2) ⭐ hay lẫn nhất

| | **Bi-encoder** (dense) | **Cross-encoder** (rerank) |
|---|---|---|
| Nhận vào | doc **RIÊNG**, query **RIÊNG** | **CẶP** `(query, doc)` cùng lúc |
| Tính sẵn lúc ingest được? | ✅ **ĐƯỢC** — mã hoá doc không cần biết query | ❌ **KHÔNG** — chưa có query thì không tính được gì |
| Lúc query phải làm gì | embed **1** câu hỏi, rồi so cosine | chạy model **1 lượt cho TỪNG doc** |
| Giá | **RẺ** | **ĐẮT** |
| Phạm vi | **RỘNG** — quét toàn kho được | **HẸP** — chỉ ~10 doc đã lọc sẵn |
| Độ chính xác | thấp hơn | **cao nhất pipeline** |

> ⚠️ **Bẫy đã mắc 2 lần:** cross-encoder là **ĐẮT + HẸP**, không phải "rẻ và rộng".
> Nó chính xác nhất **chính vì** đọc query và doc cùng lúc — và đúng cái đó khiến nó không
> pre-compute được, nên phải đắt.
>
> Câu thần chú: **tính sẵn được thì rẻ và rộng · phải chờ query thì đắt và hẹp**

---

## Cặp 5 — **RRF** vs **Cross-encoder**  (Trạm 2)

Cả hai đều "xử lý danh sách doc", nhưng khác hẳn:

| | **RRF** | **Cross-encoder** |
|---|---|---|
| Việc chính | **GỘP** 2 bảng xếp hạng thành 1 | **CHẤM LẠI** 1 danh sách |
| Có đọc nội dung doc không? | ❌ chỉ nhìn **thứ hạng** (1, 2, 3...) | ✅ đọc **text** thật của doc |
| Model? | không | có |
| Giá | ~miễn phí | đắt |
| Vị trí | **trong** `HybridRetriever` | **trong** `RerankingRetriever` (bọc ngoài) |

Thứ tự: `dense_ranked` + `bm25_ranked` → **RRF gộp** → 10 ứng viên → **cross-encoder chấm lại** → top 5.

Cross-encoder **vứt bỏ hoàn toàn** điểm RRF, chấm bằng điểm của chính nó.

---

## Cặp 6 — **Cross-encoder** vs **CRAG grader**  (Trạm 2 vs Trạm 3)

Cả hai đều "chấm điểm doc", nhưng ở 2 tầng khác nhau, trả lời 2 câu hỏi khác nhau:

| | **Cross-encoder** (`BGEReranker`) | **CRAG grader** (`OllamaGrader`) |
|---|---|---|
| Trạm | **2 — Retrieval** | **3 — CRAG** |
| Loại model | model xếp hạng nhỏ | **LLM thật** (qua Ollama) |
| Câu hỏi nó trả lời | *"doc nào liên quan **hơn**?"* | *"doc này có **thật sự** trả lời được không?"* |
| Đầu ra | list đã sort → cắt top 5 | verdict `CORRECT`/`AMBIGUOUS`/`INCORRECT` |
| Ảnh hưởng | doc **nào được chọn** | **có đi tìm lại hay không** (điều khiển luồng) |

> 🔑 **Điểm mấu chốt:** reranker **chỉ biết XẾP HẠNG**. Dù cả 10 doc đều rác, nó vẫn ngoan ngoãn
> trả về 5 doc rác *đã sắp thứ tự* — nó không có khái niệm "đám này tệ quá". **Đúng lỗ hổng đó
> là lý do CRAG tồn tại.**

---

## Cặp 7 — "song song" nghĩa (a) vs nghĩa (b)  (Trạm 2)

| | (a) song song **thời gian** | (b) độc lập **dữ liệu** |
|---|---|---|
| Nghĩa | 2 việc chạy **cùng lúc** | nhánh này không cần output nhánh kia |
| Cần gì | thread / async / `asyncio.gather` | chỉ cần cùng ăn input gốc |
| `HybridRetriever` có? | ❌ **KHÔNG** — dòng 24 xong mới tới dòng 27 | ✅ **CÓ** — cả 2 cùng ăn `query` |

Note cũ ghi "song song, KHÔNG tuần tự" → sai, đã sửa 2026-09-02.

---

## Cặp 8 — bền (đĩa) vs dễ vỡ (RAM)  (bug #25)

| Bền — sống qua restart | Dễ vỡ — mất khi restart |
|---|---|
| `data/manifest.json` (ghi ra đĩa) | `BM25Index` (RAM) |
| | `QdrantStore(":memory:")` (RAM) |
| | `InMemoryDocStore` (RAM) |

**Bug:** manifest **phát biểu về** dữ liệu mà nó **không sở hữu**. Sau restart, 3 kho rỗng nhưng
manifest vẫn giữ hash cũ → ingest lại cùng doc → hash khớp → `to_skip` tất cả → **không ghi gì**
vào 3 kho vừa rỗng → `/ingest` trả `200 OK` mà `/ask` rỗng.

---

## Nhật ký drill

| Ngày | Vòng | Kết quả | Cặp còn sai |
|---|---|---|---|
| 2026-09-03 sáng | ôn +1 (chưa drill) | **1/4** — trượt | Cặp 1 (`to_upsert`/`to_delete` — lẫn lần thứ 4), Cặp 3 (tưởng BM25 là model, cross-encoder không phải), Cặp 4 (tưởng cross-encoder "đắt và **rộng**") |
| 2026-09-03 sáng | drill vòng 1 (12 câu) | **11/12** | Cặp 8 (đảo ngược bền/dễ vỡ: trả lời "manifest mất, BM25 còn") |
| 2026-09-03 sáng | neo lại Cặp 8 + test 3 câu | **3/3** | — |

**Nhận xét 2026-09-03:** drill phân biệt ăn ngay trong 1 vòng (1/4 → 11/12). Xác nhận chẩn đoán:
đây là lỗi **phân biệt**, không phải lỗi **quên** — giải thích thêm không chữa được, ép chọn giữa
2 phương án thì chữa được. Cặp 8 phải neo bằng mẹo cụ thể mới vào:
**"có file thì sống · không file thì chết theo process"** (`cat data/manifest.json` mở được;
không hề tồn tại `bm25_index.json`; và workaround `rm data/manifest.json` phải làm **thủ công**
chính vì nó không tự mất).
