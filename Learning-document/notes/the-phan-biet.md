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

## Cặp 9 — đọc từ **`state`** vs đọc từ **closure**  (Trạm 3, phát hiện 2026-09-03 tối)

**Câu hỏi phân biệt duy nhất:** *trong thân hàm có dòng `state.get("<tên biến>")` hay không?*
Có → state. Không có, mà nó là **tham số của hàm bọc ngoài** → closure.

| | đọc từ `state` | đọc từ closure |
|---|---|---|
| Ví dụ trong `retrieve_node` | `tenant_id`, `query` | `candidate_k`, `top_k` |
| Bằng chứng trong code | có dòng `state.get(...)` ngay trong thân | **không** dòng nào `state.get(...)`; tên biến đến từ `def make_retrieve_node(..., candidate_k, top_k)` |
| Được ấn định lúc nào | **mỗi lần node được GỌI** (LangGraph đưa state mới nhất vào) | **lúc hàm được TẠO** — tức lúc `make_retrieve_node(...)` chạy |
| Chạy bao nhiêu lần trong đời server | mỗi request, mỗi vòng retry | **đúng 1 lần**, trong `build_graph()` lúc startup |
| Đổi được giữa 2 lần retry? | ✅ được (node trước return dict là ghi vào) | ❌ không — muốn đổi phải gọi lại hàm bọc ngoài, mà nó không được gọi lại |

> ⚠️ **Bẫy đã mắc (03/09 tối, đảo ngược cả 4 ô):** thấy CRAG "lẽ ra phải tìm rộng hơn" nên suy ra
> `candidate_k`/`top_k` là state, và `tenant_id`/`query` là closure — tức **suy từ ý định của
> thuật toán chứ không đọc code**. Đây đúng loại lỗi mà bài trace tồn tại để bắt: note nói "rộng
> hơn" nhưng code không hề làm.
>
> Câu thần chú: **có `state.get` thì mới đổi được · không có thì đã khắc chết từ lúc `build_graph`**
>
> Neo phụ: `build_graph()` chạy **1 lần** cả đời server → hàm `retrieve_node` cũng chỉ được đúc
> **1 lần** → mọi request dùng lại đúng cái hàm đó, mang theo đúng túi biến `10 / 5` đó.

---

## Cặp 10 — `def` vs `async def` trong FastAPI  (Trạm 4d, drill lại 2026-09-07)

⚠️ **Hai từ khoá này nói dối trắng trợn** — chữ "async" nghe như song song, nhưng nó là cái TUẦN TỰ.

| | `def` (hàm thường) | `async def` |
|---|---|---|
| FastAPI chạy nó ở đâu | **threadpool** — n luồng thật | **event loop** — đúng 1 luồng |
| Nhiều request cùng lúc | **song song thật** (parallelism) | **xen kẽ** (concurrency), chỉ nhường lượt tại `await` |
| Có lệnh chặn bên trong (`time.sleep`) | vẫn song song, luồng khác chạy tiếp | **cả server đứng xếp hàng** |
| Cần `Lock` cho state dùng chung? | ✅ CÓ — có luồng thật mới có ATM | ❌ không, nếu đoạn đọc-sửa-ghi không có `await` chen vào (nguyên tử sẵn) |

**Số đo thật, tự chạy 2026-09-07** ([drills/archive/2026-09-07-def-vs-async.py](../drills/archive/2026-09-07-def-vs-async.py)) —
2 endpoint thân giống hệt nhau, mỗi cái `time.sleep(2)`, bắn 3 request đồng thời:

```
/sync   (def)        -> 2.05s     ← 3 luồng chạy cùng lúc
/async  (async def)  -> 6.02s     ← xếp hàng, 2+2+2
```

> Câu thần chú: **`async` là nhường lượt, không phải thêm người làm.**
>
> Neo phụ: `BM25Index` cần `Lock` **chính vì** handler là `def` trần. Nếu nó là `async def` và
> đoạn đọc-sửa-ghi không có `await` nào, khoá đó đã là thừa.

⚠️ **Bẫy đã mắc (07/09, sai 4 lượt liên tiếp):** trả lời **đảo ngược có hệ thống** cả 4 câu —
kể cả ngay sau khi vừa đọc bảng nói đúng điều ngược lại. Bằng chứng sạch cho luật ở
[review-schedule.md § Luật bổ sung](./review-schedule.md) mục 2: **đọc giải thích không cài được
phân biệt.** Chỉ tự đo mới lật được nhãn. Hiểu hậu quả (kể được ví dụ ATM) ≠ nhớ được nhãn nào
gây ra hậu quả đó.

---

## Cặp 11 — trả về **CON SỐ** vs trả về **VẬT**  (gặp 3 lần trong 1 ngày, 2026-09-07)

Không phải cặp thuật ngữ RAG — đây là **thói quen tay** đang lặp lại, nên ghi vào đây để drill.

| Lần | Trả về nhầm | Người gọi thật sự cần |
|---|---|---|
| bài đóng gói (ẩn dụ) | *"giao số túi đã đầy"* | **những cái túi** — nội dung bên trong |
| [bug #30](./bug-log.md) (06/09) | `chunk_count` = số nhát cắt | **số chunk thật sự ghi vào kho** |
| `merge_pieces` (07/09) | `current_merge` — một túi (`str`) | `merges` — **danh sách** túi (`list[str]`) |

> Câu tự kiểm trước mỗi lần gõ `return`: **người gọi hàm này cần cầm cái gì trên tay?**
>
> Neo phụ: chữ ký hàm đã ghi sẵn câu trả lời. `-> list[str]` mà `return` ra `str` là sai ngay ở
> dòng đầu, không cần chạy mới biết.

Cùng họ với lỗi "gọi hàm mà không hứng giá trị trả về" (CLAUDE.md §6, đã dính 3 lần) — đều là
**đứt mạch giữa thứ hàm làm ra và thứ người gọi nhận được**.

---

## Cặp 12 — quyển **SỔ** (`manifest`) vs **KỆ HÀNG** (3 kho)  (sai 3 lần trong 1 buổi, 2026-09-09)

> Lỗi dai nhất từ trước tới nay: 07/09 sai 1 lần, 09/09 sai thêm **3 lần liên tiếp** trong cùng
> một buổi — luôn theo cùng một hướng: **gán quyết định skip cho 3 kho**. Chỉ vá được khi chạy
> thật và in ra ([drills/archive/2026-09-09-manifest-vs-kho.py](../drills/archive/2026-09-09-manifest-vs-kho.py)).

|  | `manifest` — quyển **SỔ** | `BM25Index` / Qdrant / `DocStore` — **KỆ HÀNG** |
|---|---|---|
| Vai trò trong `ingest_document` | nơi **HỎI** | nơi **RA LỆNH** |
| Dòng code | `old_doc = get_doc_manifest(manifest, …)` | `add_document` · `save` · `upsert` · `delete` |
| Có dòng nào hỏi nó "trong mày đang có gì" không? | ✅ có — chính là dòng trên | ❌ **KHÔNG MỘT DÒNG NÀO** |
| Chứa gì | `{chunk_index: hash}` | text / vector / token thật |
| Sau fix #25 sống ở đâu | `dict` trong RAM (`app.state.manifest`) | RAM cả ba |

**Ba dòng quyết định** ([pipeline.py:96-98](../../app/application/ingestion/pipeline.py#L96-L98)) —
đọc kỹ xem chúng đụng vào cái gì:
```
old_doc = get_doc_manifest(manifest, tenant_id, doc_id)   # ① hash CŨ, lấy từ SỔ
new_doc = {str(i): _hash(chunk) ...}                      # ② hash text VỪA GỬI LÊN
to_upsert, to_skip, to_delete = diff_manifest(old_doc, new_doc)   # ③ so hai dict trên
```
Chỉ có `manifest` và `chunks`. Ba kho mãi phía dưới mới xuất hiện, và chỉ để **nhận lệnh**.

**Ẩn dụ neo:** thủ kho **chỉ đọc sổ, không bao giờ ra kệ đếm**. Sổ ghi "đủ 3 thùng" → nói *"khỏi
nhập"*. Kệ bị khuân sạch lúc nào ông cũng không biết.

**Bảng số thật (đo 2026-09-09), cùng một hành động "ingest lại y hệt":**

| Tình huống trước lệnh | kết quả | BM25 sau lệnh |
|---|---|---|
| sổ rỗng, kệ rỗng | `3 / 0 / 0` | 3 chunk |
| sổ đủ, kệ đủ (không restart) | `0 / 3 / 0` | 3 chunk |
| sổ đủ, **kệ bị dọn sau lưng** | `0 / 3 / 0` | **[] rỗng** ⚠️ |
| **restart bản đã fix** — sổ chết theo kệ | `3 / 0 / 0` | 3 chunk ✅ |
| **restart kiểu cũ** — sổ sống dai hơn kệ | `0 / 3 / 0` | **[] rỗng** ⚠️ = bug #25 |

Hai dòng cuối khác nhau **đúng một chuyện**: manifest có chết theo hay không. Đó là toàn bộ nội
dung fix #25 — không phải "ghi sổ cẩn thận hơn" mà là **"cùng dễ vỡ"**, bắt sổ chết đúng lúc kệ chết.

**Điều "cùng dễ vỡ" KHÔNG chữa được** (dòng 3 của bảng): ai sửa thẳng vào kho sau lưng manifest thì
vẫn lệch. Fix chỉ bịt con đường **restart** — con đường duy nhất đã gây bug thật.

**Chốt bằng lời user (09/09):** *"con số 3 đó là láo — sổ ghi bỏ qua 3 mà kho không có gì; đáng lẽ
sổ phải rỗng theo cái kho, sổ với kho đi đúng với nhau."*

⚠️ **Vặn thêm nửa vòng:** con số `3` **không sai về số học** — trong sổ đúng là có 3 hash khớp. Cái
láo là **lời hứa** đi kèm: `chunk_skipped: 3` nghĩa là *"3 chunk này đã nằm sẵn trong kho, khỏi ghi"*,
mà vế "đã nằm trong kho" chưa bao giờ được kiểm chứng. **Đếm trên sổ, nhưng phát biểu về kho.**
Cùng bệnh với [Cặp 11](#) và `recursive_chunk` không đệ quy.

🪤 **Bẫy còn nằm sẵn:** `load_manifest` / `save_manifest` **vẫn còn** trong `pipeline.py` nhưng
**không ai gọi**. Đọc lướt thấy chúng là kết luận nhầm "manifest trên đĩa".

---

## Cặp 13 — `()` **CHẠY** vs `[]` **TRA**  (dính 3 lần trong 24h, drill 2026-09-12 khuya)

> Lịch sử: `current(piece)` (tối 11/09) · `state(query)` (00:15 12/09) · `d("x")` trong drill ép chọn
> (23:2x 12/09) — cùng một hướng sai: **dùng `()` cho chỗ chứa dữ liệu**. Lần thứ 3 mới lòi ra
> **cái luật user đang dùng**, và chính cái luật đó là thứ phải thay.

**Luật user tự nêu (SAI):** *"có dấu `:` là dict → `[]`, còn lại `()`"*.
Nó trả đúng **mọi** ô có dict nên trông như đúng, rồi gãy ở list: `separators` không có `:` → bị đẩy sang `()`.

|  | `()` — **CHẠY** | `[]` — **TRA** |
|---|---|---|
| Dùng cho | hàm · method · class | dict · list · tuple · chuỗi |
| Câu hỏi tự đặt | *"nó có chạy được không?"* | *"nó có chứa dữ liệu không?"* |
| Ví dụ trong repo | `decide(grades, …)` · `grader.grade(q, docs)` | `state["query"]` · `docs[0]` · `separators[0]` |
| Python nổ ra chữ gì khi sai | `not callable` | `not subscriptable` |

**Bảng số thật (chạy 2026-09-12, `.venv/bin/python`):**
```
separators()   -> NỔ TypeError: 'list' object is not callable
separators[0]  -> '\n\n'
ten()          -> NỔ TypeError: 'str' object is not callable
ten[0]         -> 'M'
counts()       -> NỔ TypeError: 'dict' object is not callable
counts["a"]    -> 3
decide([True]) -> 'CORRECT'
decide[True]   -> NỔ TypeError: 'function' object is not subscriptable
```
→ **Chữ trong câu nổ chính là cái luật:** `callable` = chạy được · `subscriptable` = tra được.
Dấu `:` không liên quan, nó chỉ là **cách viết** dict ra giấy.

### Cặp 13b — trong `[]` thì để **SỐ** hay để **KHOÁ CHUỖI**  (sai ngay sau khi 13 đã đúng)

User viết `docs["0"]` — chọn `[]` đúng rồi, nhưng nhét **chuỗi** vào chỗ cần **số thứ tự**.

|  | list / chuỗi | dict |
|---|---|---|
| Trong `[]` để gì | **số thứ tự**, không nháy: `docs[0]` | **đúng khoá như lúc tạo**: `counts["a"]` |
| Sai thì nổ gì | `TypeError: list indices must be integers or slices, not str` | `KeyError` |

```
docs["0"]     -> NỔ TypeError: list indices must be integers or slices, not str
docs[0]       -> 'tài liệu A'
counts[0]     -> NỔ KeyError: 0
counts["0"]   -> 'chuỗi số không'      # counts = {"a": 3, "0": "chuỗi số không"}
```
**Hai dòng cuối là chỗ neo:** cùng một dict, `counts[0]` nổ mà `counts["0"]` ra giá trị — dấu nháy
**đổi hẳn thứ đang tìm**, không phải trang trí.

---

## Cặp 14 — **một phần tử** (trước `in`) vs **cả list** (sau `in`)  (drill dict lồng, 2026-09-15 ở công ty)

> *(Claude ghi hộ theo yêu cầu user lúc học ở công ty — **chưa qua teach-back**. Buổi sau user kể
> lại bằng lời mình, đóng note, rồi mới tính là hiểu.)*

**Mô hình sai đã bóc ra, câu nguyên văn của user:** *"`q.keys()` thì sẽ ra được cái list
`["cam","xoai","oi"]`"*. User tưởng `q` là **cả** `qua`, nên đoán vòng `for` chỉ chạy 1 lượt
(bài 8, bài 9 vòng 2, và câu kiểm tra `tu["do_an"]`). Tức là **lỗi B không phải lỗi đếm lượt**,
gốc là nhầm biến lặp với cả list.

```python
qua = [{"cam": 1}, {"xoai": 2}, {"oi": 3}]
for q in qua:
    print(list(q.keys())[0])
```

|  | `qua` (đứng **sau** `in`) | `q` (đứng **trước** `in`) |
|---|---|---|
| Là gì | **list**, cả hàng hộp | **dict**, một hộp đang cầm trong lượt này |
| Có `.keys()` không | ❌ `AttributeError: 'list' object has no attribute 'keys'` | ✅ |
| Đổi theo lượt không | không | có, lượt 1 `{"cam":1}` · lượt 2 `{"xoai":2}` · lượt 3 `{"oi":3}` |

Đọc `for q in qua` thành *"với **MỖI** `q` trong `qua`"*. List có bao nhiêu phần tử thì có bấy nhiêu
lượt, và kẻ bảng bấy nhiêu dòng **trước khi** ghi output.

**Ba mẩu đi kèm, cùng buổi:**
- `list(d.keys())[0]` ra **tên key** (bên trái dấu `:`), **không ra value**. Muốn value thì dùng
  tên đó để mở: `d[ten]`. *(Bài 6 và 10 đoán `ten = "python"` / `2021`. Tự bắt được lỗi này nếu đọc
  dòng kế: `con[2021]` sẽ nổ `KeyError`, dự đoán tự mâu thuẫn.)*
- `x in dict` chỉ hỏi **key**, chỉ nhìn **một nấc** ngoài cùng, trả `True`/`False`, không đào xuống.
- `hop[...]` hỏi thứ không tồn tại thì **nổ** (`IndexError`/`KeyError`), chỉ `.get()` mới ra `None`.
  Sẽ gặp lại trong `danh_gia`: metadata của chunk có thể **thiếu** key.

**Thói quen chữa L1 (quên nấc):** đếm **hết** số cặp `[...]` trên dòng rồi mới chốt. Câu cuối vẫn quên
cặp `[0]` ngoài cùng, ghi `["cam"]` thay vì `cam`.

---

## Cặp 15 — BM25 khớp **MẶT CHỮ** ↔ dense khớp **NGHĨA**  (đảo nhãn, slot công ty 2026-09-18)

**Câu nguyên văn của user:** *"BM25 là thuật toán tìm kiếm **chính xác về ngữ nghĩa**"* — ngược hẳn.
Nguy hiểm hơn Cặp 3: Cặp 3 hỏi *"có phải model không"*, cặp này hỏi *"nó khớp theo cái gì"* — trả lời
sai vế này thì **không giải thích nổi vì sao phải có hybrid**, mà đó là câu mở đầu của mọi vòng phỏng vấn RAG.

|  | **BM25** (`BM25Index`, tự viết) | **Dense** (BGE + Qdrant) |
|---|---|---|
| Khớp theo | **mặt chữ** — token trùng nhau, đếm TF × IDF | **nghĩa** — khoảng cách giữa 2 vector |
| Hỏi `"o to"`, doc ghi `"xe hoi"` | **rỗng** — không token nào trùng | trả về được, vì 2 vector gần nhau |
| Hỏi mã lỗi `"E1042"`, tên riêng, số hiệu văn bản | **mạnh nhất** — chữ hiếm, IDF cao | dễ trượt, vector của chuỗi lạ không neo vào đâu |
| Gõ thiếu dấu cách (`"oto"`) | rỗng — khác token là khác hẳn | vẫn còn cơ hội |

**Bài đo thật (chạy `BM25Index` thật, slot công ty 18/09), kho chỉ có 1 doc `"gia xe hoi tang manh trong nam nay"`:**
```
A hỏi "xe hoi" : [('d1', 1.386)]
A hỏi "o to"   : []          ← doc NÓI VỀ ĐÚNG CÁI ĐÓ, vẫn rỗng
A hỏi "oto"    : []
```

> Mẹo nhớ: **BM25 không biết `xe hơi` với `ô tô` là một.** Nó chỉ biết đếm. Cái biết hai chữ đó
> cùng nghĩa là **model nhúng** — và đó chính là lý do tồn tại của hybrid: một nhánh bắt **chữ**,
> một nhánh bắt **nghĩa**, RRF trộn hai thứ đó lại.

**Kèm theo, cùng bài đo — `tenant` là PHÂN VÙNG chứ không phải lọc:**
```
B hỏi "xe hoi" : [('d3', 0.575)]   ← d3 nội dung Y HỆT d1, nhưng A hỏi không bao giờ thấy nó
doc_count = {'congty_A': 2, 'congty_B': 1}
```
`self.index[tenant_id][term][doc_id]` — tenant là **khoá ngoài cùng**, doc tenant khác không vào nổi
vòng lặp để được chấm điểm (`bm25_index.py:51`). Hai con số `1.386` vs `0.575` tuy chữ y hệt là vì
`doc_count` đếm **riêng từng tenant** → **IDF cũng tính riêng**. Bên Qdrant thì ngược lại: đó là
**lọc thật**, `query_filter=filter` (`qdrant_store.py:61`).

---

## Cặp 16 — **KHOÁ** vs **GIÁ TRỊ TẠI KHOÁ**  (tái phát 15/09 → 20/09 · ✅ **SẠCH 21/09**, 6/6 ép chọn)

```python
pred = {"gte": ["nam", 2015]}
op = list(pred.keys())[0]

op       -> 'gte'            # KHOÁ
pred[op] -> ['nam', 2015]    # GIÁ TRỊ TẠI KHOÁ
```

`list(d.keys())[0]` lấy **tên ngăn**. Muốn đồ trong ngăn thì phải tra thêm một nhịp: `d[<tên ngăn>]`.
Hỏi 20/09: *"`pred[op]` chứa gì?"* → user trả `"gte"`, tức trả lại chính cái khoá.
**Tay gõ đúng `pred[op][0]`, miệng nói sai** — thuộc thao tác, chưa thuộc nghĩa.
15/09 đã dính đúng bệnh này (bài 6, 10: `list(d.keys())[0]` tưởng ra value) ⇒ **lần 2, không giảng lại,
lần sau gặp là dựng bài đo ngay** (luật 09/09). Cùng họ với [Cặp 13b](#) (`[]` để số hay để khoá).

## Cặp 17 — ô **PHÉP** vs ô **KHOÁ CỐ ĐỊNH** trong tờ đơn Qdrant  (20/09 tối)

```python
{"key": "nam",          "range": {"gte": 2015}}       # ô này ĐIỀN TÊN PHÉP
{"key": "loai_van_ban", "match": {"value": "Luật"}}   # ô này LUÔN LUÔN là "value"
```

`range` nhận **tên phép** (`gte`/`lt`/…) làm khoá — phép nào điền phép nấy.
`match` **không nhận tên phép bao giờ**; khoá của nó chết cứng là `"value"`, dù đang dịch phép `eq`.
Sai 20/09 tối: đoán ra `"match": {"eq": ...}` — lấy tên phép nhét vào ô khoá cố định.

**Đây là chiều NGƯỢC của [Cặp 16](#) cùng ngày:** chiều 20/09 điền *tên trường* (`"nam"`) vào ô phép;
tối 20/09 điền *tên phép* (`"eq"`) vào ô khoá cố định. Cùng một bệnh — **chưa phân biệt ô nào
điền-theo-dữ-liệu, ô nào chết-cứng**. Đã sai 2 lần trong một ngày ⇒ theo luật 09/09, **lần sau
dựng bài đo ép chọn ngay, cấm giảng lại**.

## Cặp 18 — **tên biến** vs **tên hàm** đứng trước `(...)`  (22/09 sáng)

```python
list(d.keys())[0]        # list = HÀM có sẵn của Python -> chạy
ten_hop_ngoai(d.keys())  # ten_hop_ngoai = BIẾN -> TypeError: 'dict' object is not callable
list_out()               # list_out = BIẾN -> cùng lỗi
```

Dấu `(` đặt ngay sau một tên có nghĩa là **"gọi cái tên này như một hàm"**. Đặt tên biến vào đó
thì nổ `TypeError: '<kiểu>' object is not callable`.
**Sai 3 lần trong một buổi sáng 22/09** — lần nào cũng ở đúng chỗ đáng lẽ là `list`.
Kèm theo: `CAY["ten_hop_ngoai"]` (bọc nháy quanh tên biến → `KeyError`) — cùng một bệnh, chưa
tách được **cái tên** với **giá trị cái tên đang giữ**.
⇒ Lần sau gặp: ép chọn `list(...)` ↔ `<biến>(...)`, cấm giảng.

## Nhật ký drill

| Ngày | Vòng | Kết quả | Cặp còn sai |
|---|---|---|---|
| 2026-09-18 (tối) | Ép chọn BM25↔dense + tenant, 12 câu | **11/12** | Cặp 15 **đã lật đúng chiều** (ván 1 5/5, ván 3 3/3). Còn sai đúng 1 ô: số hiệu văn bản `15/2022/ND-CP` chọn DENSE, đúng là **BM25** (chữ hiếm → IDF cao). Vòng 1 trả **lệch đề** (CÓ/RỖNG thay vì BM25/DENSE) — lỗi đọc đề lần 3 |
| 2026-09-03 sáng | ôn +1 (chưa drill) | **1/4** — trượt | Cặp 1 (`to_upsert`/`to_delete` — lẫn lần thứ 4), Cặp 3 (tưởng BM25 là model, cross-encoder không phải), Cặp 4 (tưởng cross-encoder "đắt và **rộng**") |
| 2026-09-03 sáng | drill vòng 1 (12 câu) | **11/12** | Cặp 8 (đảo ngược bền/dễ vỡ: trả lời "manifest mất, BM25 còn") |
| 2026-09-03 sáng | neo lại Cặp 8 + test 3 câu | **3/3** | — |
| 2026-09-03 tối | Trạm 3 (chưa drill, hỏi mở) | **0/4 ô bảng** — đảo ngược hết | Cặp 9 (state ↔ closure) — cặp mới, chưa drill lần nào |

**Nhận xét 2026-09-03:** drill phân biệt ăn ngay trong 1 vòng (1/4 → 11/12). Xác nhận chẩn đoán:
đây là lỗi **phân biệt**, không phải lỗi **quên** — giải thích thêm không chữa được, ép chọn giữa
2 phương án thì chữa được. Cặp 8 phải neo bằng mẹo cụ thể mới vào:
**"có file thì sống · không file thì chết theo process"** (`cat data/manifest.json` mở được;
không hề tồn tại `bm25_index.json`; và workaround `rm data/manifest.json` phải làm **thủ công**
chính vì nó không tự mất).

| 2026-09-07 | ôn +1 ba hàng, hỏi mở | **1/3** (vòng đời trạng thái) | quyết định skip đọc **manifest** chứ không đọc 3 kho; fix #25 nói nhầm sang tầng retrieval |
| 2026-09-07 | drill ép chọn 10 câu | **7/10** | câu 3 (đọc lướt, không phải lẫn), câu 5 (`chunk_count`), câu 8 (`def` → tưởng tuần tự) |
| 2026-09-07 | drill Cặp 10, 3 câu | **0/3** — đảo ngược hết | Cặp 10 — đọc bảng xong vẫn trả lời ngược. Phải **tự đo** mới vào |
| 2026-09-07 | sau khi tự đo 2.05s/6.02s | tự giảng lại đúng | Cặp 10 ✅ vá bằng số, không phải bằng giảng |
| 2026-09-07 | `diff_manifest` 4 ca, dự đoán trước | **4/4** | — → **Cặp 1 SẠCH**, gỡ khỏi danh sách nợ (lần trước sai là đọc lướt, không phải lẫn) |

**Nhận xét 2026-09-07:** ba lỗi thật trong buổi **không có lỗi nào là lỗi quên** — đều là *đọc
lướt rồi trả lời theo cái mình tưởng đề đang hỏi*. Cùng cơ bắp với `recursive_chunk` không đệ quy,
`chunk_count` không đếm cái nó có vẻ đếm, và bài đo hôm nay in ra `0.05s` (404) mà vẫn tin là kết
quả đo. **Chậm lại ở chỗ đọc là loại chi phí rẻ nhất.**

*(Cặp 10 và 11 do Claude viết cuối buổi lúc user đã mệt — user kể lại bằng lời mình sáng 08/09,
đúng như đã làm với `03-crag.md` ngày 04-05/09.)*

| 2026-09-09 sáng | drill ép chọn 13 câu (gộp 6 mốc tới hạn) | **9/13** | câu 3 + câu 7 (đều là Cặp 12), câu 4 (lấy nhầm công thức RRF cho BM25), câu 5 (Cặp 4 — tưởng cross-encoder tính sẵn được), câu 10 (thiếu tiêu chí additive) |
| 2026-09-09 sáng | drill Cặp 12, 6 câu | **sai câu 2 + lý do câu 4** | Cặp 12 — lần thứ 3 trong buổi gán quyết định skip cho 3 kho |
| 2026-09-09 sáng | chạy thật + in ra (5 kịch bản) | tự giảng lại đúng | Cặp 12 ✅ vá bằng **số**, không phải bằng giảng — lặp lại đúng công thức đã gỡ nút ngày 04/09 và 07/09 |

**Nhận xét 2026-09-09:** lần thứ **ba liên tiếp** một cặp dai chỉ chịu vào sau khi **chạy thật và
in ra** (04/09 `candidate_k` · 07/09 `def`/`async def` · 09/09 manifest ↔ 3 kho). Ba lần đều đã
giảng bằng lời trước đó mà không ăn. **Rút thành luật: cặp nào sai tới lần thứ 2 thì đừng giảng
lần 3 — dựng bài đo ngay.** Giảng lần 3 tốn giờ và làm user nản ("khó quá", "chưa hiểu nhỉ").

⚠️ **Ghi thêm — dấu hiệu cần đổi cách, gặp thật sáng 09/09:** user nhắn *"KHÓ QUÁ BẠN KHÔNG BIẾT
CHẠY SAO"*. Không phải bí kiến thức — bí **thao tác**: câu lệnh phải đứng ở thư mục `nyxara-core`
và cần `PYTHONPATH=.`, mà terminal đang ở `Developer`. **Bài đo do Claude dựng thì Claude chạy hộ
luôn**, đừng bắt user vật lộn với đường dẫn giữa lúc đang tắc khái niệm — trộn hai loại khó vào
nhau là mất cả hai.

| 2026-09-15 công ty | drill vòng 2 dict lồng, bài 1-5 | **4/5** | L3 (bài 5 đếm `[1]` từ 1 — bài 4 cùng biểu thức lại đúng) |
| 2026-09-15 công ty | kiểm tra `mau[...]` 4 câu | **2/4** | `mau[4]` đoán `None` → thật là `IndexError` (lẫn với `.get`) |
| 2026-09-15 công ty | vòng 2 bài 6-10 | **1/5 sạch** (bài 7) | lỗi A `list(d.keys())[0]` tưởng ra value (6, 10) · lỗi B `for` chỉ đi lượt 1 (8, 9) |
| 2026-09-15 công ty | chạy thật + in từng lượt | lỗi B lòi gốc | Cặp 14 — tưởng `q` là cả `qua` |
| 2026-09-15 công ty | `so` + `qua` điền bảng lượt | **đúng** 2 cột `q` / `keys` | còn quên cặp `[0]` ngoài cùng ở cột "in ra" (L1 nhẹ) |
| 2026-09-21 công ty | ép chọn Cặp 16+17, 10 câu | **9/10** | sai đúng câu `match` ⇒ **Cặp 17**. ⭐ **Cặp 16 SẠCH** — 6/6 khoá↔giá trị, kể cả câu lồng 2 nhịp `d[list(d.keys())[0]]` |
| 2026-09-21 công ty | Cặp 17 sau khi đo bằng Qdrant thật (`MatchValue(eq=...)` nổ `value Field required`) | **2/2** | chưa coi là sạch — xen lại 2 câu đầu buổi sau |
| 2026-09-22 sáng | Cặp 17 xen đầu buổi, 2 câu | **1/2** | sai lại đúng ô `match` (chọn `"eq"`). Chưa sạch sau 1 ngày |
| 2026-09-22 sáng | Cặp 17 sau bài đo Qdrant thật (vòng 2: `eq` trên **số** cũng nổ) | **3/3** | chữ *"chuỗi"* trong tiêu chí của user là thứ làm hỏng — `match` chết cứng `"value"` bất kể chuỗi hay số |

**Nhận xét 2026-09-15:** lỗi B sai 2 lần khi giảng bằng lời, chỉ bóc ra gốc khi user **tự nói ra cách
mình đang nghĩ** (*"`q.keys()` ra `["cam","xoai","oi"]`"*) — rồi chạy thật in từng lượt là vào ngay.
Đúng luật 09/09: sai lần 2 thì dựng bài đo, đừng giảng lần 3.
