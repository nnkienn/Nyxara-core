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
| 2 | [02-retrieval.md](./02-retrieval.md) | `retrieval/hybrid_retriever.py` + `reranking_retriever.py` | ✅ 2a,2b,2c xong + teach-back qua cổng (2026-09-02) |
| 3 | [03-crag.md](./03-crag.md) | `generation/node.py` + `decision.py` + `graph.py` | 🔨 2026-09-03 sáng: xong phần **khái niệm closure vs state** + bảng "nguồn của 4 biến". Bảng trace lần-2 ⬜ chưa làm — vào thẳng đó ca tối |
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

**2a.** ✅ *TRẢ LỜI 2026-09-02.* Thân `HybridRetriever.search` **không có** thread/async/
`asyncio.gather` nào — dòng 24 (`dense_hits`) chạy xong mới tới dòng 27 (`bm25_hits`). Code chỉ
thoả nghĩa **(b) độc lập dữ liệu** (cả 2 ăn `query` gốc, không nhánh nào cần output nhánh kia),
KHÔNG thoả nghĩa **(a) song song về thời gian**. → Note SAI: chữ "song song, KHÔNG tuần tự" gợi
nghĩa (a). Note *định* nói "2 nhánh độc lập, thứ tự không quan trọng" nhưng diễn đạt thành "chạy
đồng thời". **Đã sửa note `02-retrieval.md` 3 chỗ** (bước "Kể chuyện" #2, sơ đồ, điểm 1 phần "5
điểm dễ hiểu nhầm"). Ghi chú: vì độc lập dữ liệu nên *có thể* đưa lên thread chạy song song thật
để giảm latency — khoảng trống tiềm năng, chưa làm.

**2b.** ✅ *TRẢ LỜI 2026-09-02.* Gọi `RerankingRetriever.search(candidate_k=10, top_k=5)`:

| Chặng | Số | Vì sao |
|---|---|---|
| Qdrant được hỏi | 20 | `candidate_k=10` truyền **theo vị trí 3** → rơi vào param tên `top_k` của Hybrid → dòng 21 `candidate_k = top_k * 2` = 20 |
| BM25 được hỏi | 20 | cùng biến `candidate_k=20` nội bộ Hybrid |
| RRF trả về | 10 | `top_k=top_k` = 10 |
| `doc_store.get` trong Reranking | 10 lượt | 1 lượt/candidate |
| Cross-encoder chấm | 10 cặp | = số candidate ra khỏi Hybrid |
| Kết quả cuối | 5 | `reranked[:top_k]`, `top_k=5` lớp ngoài |

→ Bài học: `candidate_k=10` caller đặt **không** phải số Qdrant thấy (20 — Hybrid tự nhân đôi
lần nữa). Tên `candidate_k` ngoài → chui vào `top_k` trong → lớp trong tự chế `candidate_k`
riêng. **Đọc code phải bám vị trí tham số, không tin tên biến.**

**2c.** ✅ *TRẢ LỜI 2026-09-02.* `RerankingRetriever.search` trả `list[tuple[doc_id, score]]` —
**không có text**. Nên `retrieve_node` ([node.py:25](../../../app/application/generation/node.py#L25))
phải gọi `doc_store.get` **lại lần nữa**. Đếm 1 lần `/ask`: 10 lượt (Reranking) + 5 lượt (node)
= **15 lượt**; riêng 1 `doc_id` lọt top 5 bị đọc **2 lượt**.
→ **Gốc rễ:** không phải node "muốn" lấy lại, mà **hình dạng return không mang text đi được**.
→ **Không sửa bằng cách đổi mình `RerankingRetriever`** (trả 3-tuple) — sẽ nổ `ValueError: too
many values to unpack` ở `node.py` dòng 24, và làm 2 retriever lệch hình dạng → mất tính thay
thế được (`retrieve_node` nhận `retriever` qua tham số, không biết mình cầm Hybrid hay Reranking).
→ **Cách đúng (C):** đổi hình dạng return cho **CẢ HAI** retriever cùng lúc, vd `RetrievedDoc(id,
score, text)`. Hợp đồng vẫn đồng nhất, và `retrieve_node` lấy `doc.text` thẳng — 5 lượt thừa biến mất.
→ **Quyết định giai đoạn này: để nguyên.** `InMemoryDocStore.get` là tra dict RAM (~µs), 5 lượt
thừa không đáng đổi hợp đồng. Chỉ đáng sửa khi `DocStore` ra mạng (Postgres/S3) = 5 round-trip thừa.

**Chốt khái niệm hay lẫn (làm rõ 2026-09-02):** trong Trạm 2 chỉ **2/4** thành phần là model AI.
`RRF` = toán thuần `1/(k+rank)`, gộp 2 bảng xếp hạng, không đọc nội dung doc, gần như miễn phí.
`BM25` = thống kê TF/IDF, không phải model. `Bi-encoder` = model, **vector doc tính sẵn lúc
ingest** nên rẻ khi query. `Cross-encoder` = model, **ĐẮT và HẸP** — phải chạy 1 lượt forward cho
**từng cặp** `(query, doc)`, và **không pre-compute được** vì cần cả query lẫn doc cùng lúc (1
triệu chunk = 1 triệu lượt chạy model cho 1 câu hỏi). → Kiến trúc **rẻ-rộng lọc 1tr → 10, rồi
đắt-hẹp chấm kỹ 10 đó → lấy 5**. Và **cross-encoder KHÔNG thuộc CRAG**: nó chỉ biết *xếp hạng*,
không bao giờ nói "cả đám này đều tệ, đi tìm lại" — đúng lỗ hổng đó là lý do CRAG (Trạm 3) tồn tại.

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

**Nền tảng — closure vs state.** ✅ *Làm xong 2026-09-03 sáng, bằng Python thuần trước
(`make_multiplier`/`make_greeter`), chưa đụng CRAG.* Ý chính: hàm trong lấy dữ liệu từ **2 nguồn**
— *tham số* (đổi được mỗi lần gọi) và *closure* (chụp lúc hàm ngoài chạy, **đông cứng vĩnh viễn**,
không có đường truyền giá trị mới vào; gán lại biến trùng tên ở scope ngoài **vô hiệu** vì đó là
biến khác). Muốn đổi giá trị closure → **phải gọi lại hàm ngoài để dựng hàm mới**.

**Cột nguồn — ✅ đã điền 2026-09-03 sáng:**

| Input của `retriever.search` | Lấy từ `state` hay closure? | Bằng chứng trong code |
|---|---|---|
| `tenant_id` | **state** | có dòng `tenant_id = state.get("tenant_id")` |
| `query` | **state** | có dòng `query = state.get("query")` |
| `candidate_k` | **closure** | **KHÔNG** có dòng `state.get("candidate_k")` — nó là tham số của `make_retrieve_node` |
| `top_k` | **closure** | **KHÔNG** có dòng `state.get("top_k")` — tham số của `make_retrieve_node` |

**Câu hỏi ⚠️ ĐÃ LÀM ca tối 2026-09-03 — trả lời SAI, đã được sửa, nhưng CHƯA qua cổng.**
`retrieve_node` chạy **lần 2** (sau khi grade ra `INCORRECT`) — mỗi input đến từ `state` hay
closure, và lần 2 giống hay khác lần 1?

| Input của `retriever.search` | Nguồn | Lần 2 vs lần 1 | User trả lời (03/09 tối) |
|---|---|---|---|
| `tenant_id` | **state** (`state.get("tenant_id")`) | giống (cùng 1 request) | ❌ nói là closure |
| `query` | **state** (`state.get("query")`) | giống (cùng 1 request) | ❌ nói là closure |
| `candidate_k` | **closure** (tham số `make_retrieve_node`, không có `state.get`) | **giống — bắt buộc giống** | ❌ nói là state, "CRAG retry sẽ mở rộng ra" |
| `top_k` | **closure** (cùng lý do) | **giống — bắt buộc giống** | ❌ nói là state |

→ **Đảo ngược cả 4 ô.** Lỗi cùng loại với 4 lỗi mốc ôn +1 sáng cùng ngày: lẫn 2 khái niệm na ná
(state ↔ closure), không phải quên. Cần thêm 1 cặp vào [the-phan-biet.md](../the-phan-biet.md).

**Kết luận đúng của trạm này (đã giải thích, user xác nhận hiểu phần cơ chế):**
`build_graph()` chỉ chạy **1 lần** lúc server start → `make_retrieve_node(...)` được gọi **1 lần**
→ `candidate_k=10`, `top_k=5` bị khắc chết vào túi biến closure của **đúng 1** hàm `retrieve_node`
dùng lại cho mọi request + mọi lần retry. Không có đường ghi giá trị mới vào (thân hàm không hề
gọi `state.get("candidate_k")`). Vậy 4 input lần 2 y hệt lần 1 → `retrieved_docs` y hệt →
`verdict` y hệt (`INCORRECT`) → **chữ "tìm rộng hơn" trong [03-crag.md](./03-crag.md) là thứ ĐỊNH
làm mà code CHƯA làm** (note nói dối). Vòng lặp không bao giờ tự khá lên; nó chỉ thoát bằng **van
an toàn `attempts >= max_attempts`** trong [decision.py](../../../app/application/generation/decision.py)
`route()`, rồi generate trên đúng đám docs vừa bị chê 3 lần.

**Cách sửa (đã suy luận đúng hướng, chưa code):** `retrieve_node` đọc
`candidate_k = state.get("candidate_k", candidate_k)` (closure tụt xuống làm default lần đầu)
**và** `grade_node` — nơi sinh ra `verdict`, nơi đã `attempts + 1` — là node phải return
`candidate_k` lớn hơn khi verdict là `INCORRECT`. User đầu tiên trả lời "node retrieve ghi" →
chạy được về máy nhưng sai nhà: `retrieve_node` không hề thấy `verdict`, nới rộng là **hệ quả của
1 vòng thất bại** nên phải nằm cùng chỗ với bộ đếm thất bại.

**✅ 2026-09-04 (21:42-23:30) — TRẠM 3 XONG PHẦN HIỂU.** Đường đi tới đó:
- Ôn bù 2 hàng treo: **9.5/10** (hôm trước 1/4) → đã tick mốc +3.
- Drill Cặp 9 (state↔closure) 2 vòng: vòng 1 sai 3/7 câu then chốt, vòng 2 vẫn sai `max_attempts`
  (đoán state, thực ra closure) và sai 4/5 dòng bài đoán output closure thuần Python.
- **Chỗ tắc thật, mất 3 lượt mới lòi ra:** user không biết `build_graph()` **chạy lúc nào** —
  hỏi thẳng "chạy hồi nào?". Thiếu mảnh **vòng đời app**, không phải thiếu hiểu closure. Gỡ bằng
  `main.py` lifespan (trước `yield` = chạy 1 lần lúc boot) + `ask.py:22` (handler chỉ *lấy lại*
  `request.app.state.graph`, không dựng lại).
- **Cái thật sự gỡ được nút:** thôi bắt user *tưởng tượng* vòng lặp, chuyển sang **cho chạy thật
  và in ra**. Chạy `build_graph` thật + 3 node thật, chỉ thay 4 adapter ngoài rìa bằng đồ giả
  (grader luôn `False`), in `candidate_k` mỗi lượt. Ba dòng `candidate_k=10` giống hệt nhau nói
  thẳng điều mà 3 lượt giải thích trước đó không nói được. **Ghi nhớ cách này cho các trạm sau:
  quan sát trước → giải thích sau, khi dự đoán đã trượt 2-3 lần liên tiếp.**
- Câu chốt xác nhận đã hiểu (user tự trả lời đúng): *"request thứ hai tới thì `candidate_k` là
  bao nhiêu?"* → vẫn 10, vì hàm được đẻ ra **trước mọi request**.
- User tự phát biểu được hậu quả: trả tài liệu rác cho người dùng, **dù hệ thống tự biết là rác**.

**⚠️ Ghi chú trung thực:** phần sửa note `03-crag.md` + [bug #26](../bug-log.md) là **Claude viết**,
không phải user viết bằng lời mình (user xin hỗ trợ để kịp giờ, hẹn trace lại 05/09). Vậy 2 file
đó **chưa tính là đã qua bước 6 DOCUMENT** — 05/09 phải đọc lại và tự kể lại bằng lời mình.

**✅ 2026-09-05 — TRẠM 3 ĐÓNG HOÀN TOÀN (hiểu + làm).** Bản fix bug #26 đã code xong bằng tay,
có test riêng (`test_retry_noi_rong_candidate_k`) và đã kiểm chứng test đỏ đúng lúc phải đỏ.
Chi tiết đầy đủ: [bug-log #26](../bug-log.md) · bug phụ sinh ra trong lúc fix: #28 (UnboundLocalError).

**⬜ Còn nợ nhỏ của trạm này (làm khi có thời gian, không chặn Trạm 4):**
- Test nhánh ngược: verdict `CORRECT` ngay vòng 1 → retriever chỉ được gọi **đúng 1 lần**.
- Cân nhắc: vòng cuối `grade_node` vẫn ghi `candidate_k=80` dù `route()` đã hết lượt và không ai
  đọc nữa — có nên ghi khi biết chắc không còn vòng nào không?
- Chọn lại giá trị mặc định trong `state.get("candidate_k", 0)` — với công thức `* 2` thì `0`
  là lựa chọn tệ nhất có thể (`0 * 2 = 0` mãi mãi).

**(lưu trữ) ⬜ Danh sách nợ ghi tối 04/09:**
1. **CODE TAY bản fix bug #26** (2 nửa: `retrieve_node` đọc `candidate_k` từ state ·
   `grade_node` ghi giá trị lớn hơn khi `INCORRECT`) + **2 test regression** (test phải bắt được
   dãy `candidate_k` qua từng vòng là tăng dần, không phải chỉ nhìn output cuối). Xem
   [bug-log #26](../bug-log.md) mục *Fix* và *Test chặn tái phát*.
2. **Tự kể lại** nội dung bug #26 + đoạn sửa trong `03-crag.md` bằng lời mình (2 file đó hiện do
   Claude viết, chưa qua bước DOCUMENT thật).
3. Ôn lại **Cặp 9** — vòng 2 vẫn còn sai `max_attempts` và bài closure thuần Python.
4. Sau đó mới mở **Trạm 4 (API)** — 4a…4d chưa đụng.

> Ghi chú phương pháp (rút ra tối 03/09): 2 lần liên tiếp mình gộp nhiều tầng suy luận vào 1 lượt
> hỏi (teach-back 2 ý cùng lúc) → user tắc ngay, đúng lỗi §3.6 mục 6 đã vá 01/09. Lần sau ở trạm
> này: 1 ô bảng / 1 câu, số thật, không hỏi "vì sao" trừu tượng khi cơ chế chưa vững.

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
