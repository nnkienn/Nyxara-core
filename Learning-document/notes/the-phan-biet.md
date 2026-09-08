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

**Số đo thật, tự chạy 2026-09-07** ([drills/2026-09-07-def-vs-async.py](../drills/2026-09-07-def-vs-async.py)) —
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
> thật và in ra ([drills/2026-09-09-manifest-vs-kho.py](../drills/2026-09-09-manifest-vs-kho.py)).

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

## Nhật ký drill

| Ngày | Vòng | Kết quả | Cặp còn sai |
|---|---|---|---|
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
