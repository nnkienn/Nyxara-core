# 0️⃣ Bài tập trace — tự kiểm tra hiểu luồng

> **Cách dùng:** mở song song 2 cửa sổ — một bên note (`01`→`04`), một bên code. Trả lời bằng
> cách **đọc thân hàm**, KHÔNG đọc tên hàm, KHÔNG tin sơ đồ trong note.
>
> **Luật:** 4 file note `01`–`04` do Claude viết, **không phải chân lý**. Trong đó có ít nhất
> **3 chỗ mô tả LỆCH với code thật đang chạy** — có chỗ sai chữ, có chỗ sai tới mức một tính năng
> bạn tưởng đang hoạt động thì thực ra không. Nhiệm vụ là **bắt cho ra**.
>
> Bắt đầu: 2026-08-25 (Fedora). File này để mang context sang máy khác.

## Bản đồ 4 trạm

| Trạm | Note | Code mở kèm | Xong? |
|---|---|---|---|
| 1 | [01-ingest.md](./01-ingest.md) | `ingestion/pipeline.py` + `chunking/recursive_chunker.py` | ✅ 1a,1b,1c xong + teach-back qua cổng đóng-sách (2026-09-02, retrace theo Method 2.0) |
| 2 | [02-retrieval.md](./02-retrieval.md) | `retrieval/hybrid_retriever.py` + `reranking_retriever.py` | 🔨 bắt đầu 2026-09-02 — đang ở 2a |
| 3 | [03-crag.md](./03-crag.md) | `generation/node.py` + `decision.py` + `graph.py` | ⬜ |
| 4 | [04-api.md](./04-api.md) | `app/main.py` + `presentation/api/*.py` | ⬜ |

---

## 🚩 TRẠM 1 — Ingest

**1a.** ✅ *TRẢ LỜI 2026-09-01 (retrace, teach-back trôi chảy).* `ingest.py` gọi
`recursive_chunk`, KHÔNG phải `split_by_separators`. Thân `recursive_chunk` là vòng `while`
tuần tự (fixed-size sliding window: `end = start + size`, `start = end - overlap`) — **không
có đệ quy nào cả**, cắt mù theo số ký tự, không biết ranh giới từ/câu. Tên "recursive" nói dối
hành vi thật ("tên hàm nói dối hành vi"). Hậu quả: benchmark "Recursive vs Semantic" ở Phase 3
sẽ so **sai baseline** (thực chất so Fixed-size vs Semantic).

**1b.** ✅ *TRẢ LỜI 2026-09-01.* `grep -rn "split_by_separators" app/ tests/` → chỉ 4 chỗ: định
nghĩa, tự gọi chính nó (đệ quy thật), import test, gọi trong test. **Không có call site nào
trong `app/`.** → Hàm mồ côi: viết xong, có test xanh, nhưng chưa nối vào pipeline. Bài học:
test xanh chứng minh hàm *tính đúng*, KHÔNG chứng minh hàm *được dùng* trong hệ thống thật.
Cùng họ bẫy với 1a: một "vật chứng" (tên gọi / test xanh) khiến tin nhầm điều không đúng về
hệ thống đang chạy.

**1c.** ✅ *Phần 1 (bảng trace) xong 2026-09-01. Phần 2 (i/ii/iii) xong 2026-09-02.*
Chốt: `to_skip` **không xuất hiện trong vòng lặp nào** là CHỦ Ý, không phải thiếu sót —
"không làm gì" = không gọi lại `embedder.embed` (dòng 106, dòng đắt nhất: chạy model) trên
nội dung không đổi. Đó là toàn bộ lý do incremental ingest tồn tại. `to_delete` cần vòng lặp
(chủ động dọn rác), `to_upsert` cần vòng lặp (ghi), `to_skip` = phần còn lại tự hưởng lợi bằng
cách bị lờ đi. Ví dụ đã trace: re-ingest 5 lần nội dung không đổi → bản đúng embed `"mèo"` 1
lần, bản phá logic embed 5 lần → thừa 4.
Cũng làm rõ (chỗ từng vấp 3 lần): `to_delete` **chỉ** chứa index string bị **biến mất hẳn** ở
lần sau (doc ngắn đi) — không bao giờ chứa hash, không dính "đổi nội dung tại chỗ" (cái đó →
`to_upsert` vì cùng index, khác hash). Và vì sao manifest lưu **hash** chứ không phải danh
sách index: chỉ lưu index thì bỏ sót **sửa nội dung tại chỗ** (`"chó"→"vịt"` cùng index `"1"`
→ diff tưởng không đổi → bản mới không bao giờ được ghi).

Tenant `t1`, doc `d1`. Bảng đã điền:

*Lần ingest 1:* `chunks = ["mèo", "chó", "gà"]`, `old_doc = {}`

| | giá trị |
|---|---|
| `new_doc` | `{"0": Hm, "1": Hc, "2": Hg}` |
| `to_upsert` / `to_skip` / `to_delete` | `["0","1","2"]` / `[]` / `[]` |

*Lần ingest 2:* sửa chunk giữa → `chunks = ["mèo", "vịt", "gà"]`

| | giá trị |
|---|---|
| `old_doc` | `{"0": Hm, "1": Hc, "2": Hg}` (= `new_doc` lần 1) |
| `new_doc` | `{"0": Hm, "1": Hv, "2": Hg}` |
| `to_upsert` / `to_skip` / `to_delete` | `["1"]` / `["0","2"]` / `[]` |

(Lỗi vòng đầu: từng ghi `to_delete=[(1,"chó")]` — sai, vì chỉ số `"1"` **vẫn còn** trong `new_doc`
lần 2, chỉ đổi nội dung → `to_upsert`, không phải `to_delete`. `to_delete` chỉ khác `[]` khi lần
sau **mất hẳn** một chỉ số so với lần trước.)

Rồi trả lời (⬜ còn dở — tiếp tục buổi sau):
- **(i)** Lần 2, chunk `"0"` (`"mèo"`) nằm trong `to_skip`. **Ngay lúc đó 3 kho đang chứa gì về chunk `"0"`?**
- **(ii)** Nếu 3 kho đã có sẵn và nội dung không đổi — muốn chương trình làm gì? Ghi đè? Xoá? Không làm gì?
- **(iii)** Dòng nào trong `ingest_document` **tốn tiền/thời gian nhất**? (dòng nào phải chạy một
  model AI thật?) Nhét `"mèo"` vào `to_upsert` thay vì `to_skip` thì dòng đó chạy thừa bao nhiêu lần?

→ Trả lời xong sẽ tự thấy vì sao `to_skip` **không xuất hiện lần nào nữa** trong thân hàm,
và vì sao đó **không** phải thiếu sót.

---

## 🚩 TRẠM 2 — Retrieval

**2a.** Note viết đậm 2 chỗ: *"chạy **song song**, KHÔNG tuần tự"*. Đọc thân
`HybridRetriever.search` — có `thread` / `async` / `await` / `asyncio.gather` nào không?
Dòng `bm25_hits = ...` chạy **trước hay sau** khi `dense_hits` có kết quả?
→ Note đúng hay sai? Nếu sai, note *định* nói gì mà diễn đạt hỏng?
> Gợi ý hướng nhìn: "song song" có 2 nghĩa — song song về **thời gian chạy**, và độc lập về
> **dữ liệu đầu vào**. Note đang nói nghĩa nào, code thoả nghĩa nào?

**2b.** Hợp đồng giữa 2 lớp — đọc chậm:
- `RerankingRetriever.search(tenant_id, query, candidate_k, top_k)` — 4 tham số
- nó gọi `self.hybrid_retriever.search(tenant_id, query, candidate_k)`
- nhưng chữ ký là `HybridRetriever.search(tenant_id, query, top_k)`

→ Biến tên `candidate_k` ở lớp ngoài rơi vào tham số tên gì ở lớp trong? Dòng đầu thân
`HybridRetriever.search` làm gì với con số vừa nhận?
→ Với `candidate_k=10, top_k=5`: **Qdrant được hỏi bao nhiêu ứng viên? RRF trả về bao nhiêu?
Cross-encoder chấm bao nhiêu cặp?** Tính ra 3 con số cụ thể.

**2c.** `RerankingRetriever.search` lấy `texts` từ `doc_store`, nhưng dòng `return` trả về gì —
có `text` trong đó không? Rồi mở `node.py::retrieve_node` — nó làm gì ngay sau khi nhận kết quả?
→ Trong 1 lần `/ask`, `doc_store.get()` bị gọi **mấy lượt cho cùng một `doc_id`**?
Cố ý hay lãng phí? Nếu lãng phí, sửa `RerankingRetriever` hay sửa `retrieve_node` mới đúng chỗ?
(Nghĩ theo hướng: đổi cái nào thì **phá hợp đồng của ai**.)

---

## 🚩 TRẠM 3 — CRAG  ⚠️ chỗ lệch nghiêm trọng nhất nằm ở đây

Mở 3 thứ này cùng lúc:

**(1)** [03-crag.md](./03-crag.md) — "Kể chuyện trước", bước 4:
> *"**Tệ** (`INCORRECT`) → quay lại `retrieve`, tìm **rộng hơn**, rồi `grade` lại."*

**(2)** `graph.py`, với default `candidate_k=10, top_k=5`:
```python
retrieve_node = make_retrieve_node(retriever, doc_store, candidate_k, top_k)
```

**(3)** `node.py`:
```python
def make_retrieve_node(retriever, doc_store, candidate_k, top_k):
    def retrieve_node(state):
        tenant_id = state.get("tenant_id")
        query = state.get("query")
        candidate_docs = retriever.search(tenant_id, query, candidate_k, top_k)
```

**Câu hỏi:** `retrieve_node` chạy **lần 2** (sau khi grade ra `INCORRECT`). Điền *"giống lần 1"*
hoặc *"khác lần 1"*:

| Input của `retriever.search` | Lần 2 vs lần 1 | Lấy từ `state` hay từ closure? |
|---|---|---|
| `tenant_id` | ? | ? |
| `query` | ? | ? |
| `candidate_k` | ? | ? |
| `top_k` | ? | ? |

> Chú ý: `candidate_k`/`top_k` **không nằm trong `state`** — bị đông cứng trong closure từ lúc
> `build_graph` chạy, mà graph chỉ build **1 lần duy nhất** lúc server khởi động (`main.py` lifespan).

→ Nếu cả 4 input y hệt lần 1, và retriever là hàm thuần (cùng input → cùng output), thì
`retrieved_docs` lần 2 **khác gì** lần 1? `grade` lần 2 ra verdict gì? Vòng lặp kết thúc bằng cách nào?
→ So với chữ **"tìm rộng hơn"** trong note: note đang mô tả thứ code **đang làm**, hay thứ bạn
**định làm mà chưa làm**?
→ Nếu muốn "rộng hơn" thành thật, `candidate_k` phải chuyển từ đâu sang đâu?

---

## 🚩 TRẠM 4 — API / wiring

**4a.** `lifespan` trong `main.py` chạy **mấy lần** trong đời một process? Nó dựng bao nhiêu
instance `BM25Index`? Nếu **2 request `/ingest` tới cùng lúc**, chúng ghi vào **cùng một** object
`BM25Index` hay 2 object khác nhau? (Nhớ: handler viết `def` → FastAPI chạy nó trong
**threadpool nhiều luồng**.) → Có vấn đề gì không? Từ khoá tra cứu: *race condition*, *thread-safety*.

**4b.** `/ingest` trả về `chunk_count = len(chunks)`. Nhưng `ingest_document` bên trong có thể
xếp phần lớn chunk vào `to_skip` và **không ghi gì cả**.
→ `chunk_count` đang trả lời câu hỏi nào: *"cắt ra bao nhiêu chunk"* hay *"ghi vào kho bao nhiêu chunk"*?
→ Client đọc con số đó sẽ **hiểu nhầm** thành cái nào? Muốn trung thực thì `ingest_document`
phải **trả về** cái gì mà hiện tại nó đang trả về `None`?

**4c.** Bug #25 — vòng đời lệch pha. Liệt kê 4 nơi giữ trạng thái trong `main.py` lifespan, ghi
rõ mỗi cái sống ở đâu (RAM hay đĩa) và **chết khi nào**.
→ Cái nào đang **phát biểu về** dữ liệu mà nó **không sở hữu**?
→ Có 2 cách làm cho nhất quán: cùng bền, hoặc cùng dễ vỡ. Mỗi cách phải sửa gì? Cách nào hợp
với giai đoạn hiện tại của dự án?
→ Test chặn tái phát phải giả lập được điều gì? (từ khoá: *ephemeral vs durable*, *source of truth*, *staleness*)

**4d.** Vì sao 2 handler viết `def` mà không `async def`? Nếu đổi thành `async def` mà bên trong
vẫn gọi `graph.invoke()` (đồng bộ, chặn) thì chuyện gì xảy ra với **các request khác**?

---

## Sau khi xong 4 trạm

1. Sửa lại các chỗ note sai — **viết bằng lời của mình**, đừng chép lại.
2. Ghi bug mới tìm được vào [../bug-log.md](../bug-log.md) (đủ: triệu chứng → nguyên nhân → cách
   tìm ra → fix → **pattern tổng quát**).
3. Cập nhật trạng thái thật vào [../../LEARNING_ROADMAP.md](../../LEARNING_ROADMAP.md).
