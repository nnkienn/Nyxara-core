# 🧮 Algorithms — thuật toán, toán & CTDLGT

> Nơi ghi **kiến thức lõi** của mỗi kỹ thuật: công thức, WHY, độ phức tạp, và bài CTDLGT
> ẩn bên trong. Viết lại bằng lời của mình sau khi code tay — nếu chưa giải thích được
> bằng số thật thì **chưa hiểu**, quay lại bước 1.

**Template cho mỗi kỹ thuật:**
```
### <Tên>  ·  Phase <n>  ·  <ngày>
- **Bài toán nó giải:** …
- **Công thức / thuật toán:** … (viết ra, không link đi nơi khác)
- **Ví dụ bằng SỐ THẬT:** … (tự bịa 2–3 số, chạy công thức tay)
- **CTDLGT bên trong:** … (hash map? heap? graph?) + độ phức tạp O(?)
- **Bẫy dễ sai:** … (thường trùng với bug cố ý ở [[bug-log]])
- **Khi nào đáng bật (flag):** …
```

---

## Bảng CTDLGT ↔ kỹ thuật (bản đồ nhanh)

| Cấu trúc | Kỹ thuật RAG | Phase |
|---|---|---|
| Hash map / inverted index | BM25 (term→postings), dedup | 0, 2 |
| Priority queue / heap | top-k, MMR | 2 |
| Sliding window | chunking, context budgeting | 0, 2 |
| Trie / prefix tree | tokenizer, PII matching | 0, 5 |
| Graph (BFS/DFS) | LangGraph state machine, GraphRAG | 2, 4 |
| Quy hoạch động (DP) | edit distance (near-dup dedup) | 0 |
| Two-pointer / merge | RRF (gộp N ranked list) | 2 |

---

## (Điền kiến thức từng kỹ thuật bên dưới khi học — Phase 0 trở đi)

### Recursive chunking · Phase 0 · 2026-07-14

- **Bài toán nó giải:** Khi cần cắt một đoạn văn bản dài mà không làm mất ngữ nghĩa.

- **Công thức / thuật toán:** Đệ quy + overlap. Ưu tiên cắt theo thứ tự separator từ "mạnh" đến "yếu":
  1. Cắt ở chỗ cách đoạn (2 dòng trống `\n\n`) trước — chắc chắn 2 đoạn khác nhau, an toàn nhất.
  2. Nếu 1 đoạn vẫn còn quá dài → cắt tiếp ở chỗ xuống dòng thường (`\n`).
  3. Nếu 1 dòng vẫn còn quá dài → cắt ở khoảng trắng giữa 2 từ (` `).
  4. Bí quá mới cắt ngang giữa chữ.
  5. Sau khi có các mảnh, áp `overlap`: chunk sau lấy lại vài ký tự/từ cuối của chunk trước —
     `start[chunk sau] = end[chunk trước] - overlap`.

- **Ví dụ bằng SỐ THẬT:**

  Đoạn văn gốc — cắt theo cách-đoạn trước, ra 2 đoạn (Mèo / Chó); nếu đoạn nào còn dài mới cắt
  tiếp xuống dòng:
  ```
  Mèo là loài vật đáng yêu.
  Mèo thích ngủ cả ngày.

  Chó thì trung thành với chủ.
  Chó thích chạy nhảy.
  ```

  Ví dụ overlap (tính theo **từ** cho dễ hình dung — code thật sẽ tính theo **ký tự**, ý tưởng y hệt):
  ```
  Text: "Mèo thích ngủ cả ngày và mèo cũng thích chơi bóng"
  Đánh số từ: 0:Mèo 1:thích 2:ngủ 3:cả 4:ngày 5:và 6:mèo 7:cũng 8:thích 9:chơi 10:bóng

  size = 5 từ, overlap = 2 từ

  chunk0  = từ [0:5] = "Mèo thích ngủ cả ngày"
  start1  = end0 - overlap = 5 - 2 = 3
  chunk1  = từ [3:8] = "cả ngày và mèo cũng"

  → phần chung "cả ngày" (từ 3-4) nằm ở cuối chunk0 và đầu chunk1
  ```

- **CTDLGT bên trong:** Đệ quy (recursion) + sliding window (overlap). Độ phức tạp: O(n).

- **Bẫy dễ sai:** Nếu `overlap >= size` thì không còn ký tự mới nào để ghép — chunk không tiến
  lên được (đứng yên hoặc lặp vô hạn).

- **Khi nào đáng bật (flag):** _(điền sau khi code xong)_



## Dedup (exact) — Phase 0

- **Bài toán nó giải:** loại bỏ các chunk **trùng hệt nhau** trước khi nạp kho. Chunk trùng
  gây 2 hại: (1) khi retrieval, các bản trùng chiếm hết slot top-k → đẩy chunk khác ra → câu
  trả lời nghèo đi; (2) tốn tiền embed nhiều lần cho cùng một nội dung. Còn giúp ingest
  **idempotent** (chạy lại cùng doc không nhân đôi).

- **Công thức / thuật toán:** giữ 1 `set` tên `seen`. Duyệt từng chunk theo thứ tự — **kiểm
  tra trước** (`chunk not in seen`?): nếu chưa gặp → thêm vào `result` **và** `seen.add`; nếu
  gặp rồi → bỏ qua. Phải kiểm tra TRƯỚC rồi mới add (add trước sẽ bỏ nhầm ngay bản đầu tiên).

- **Ví dụ (người gác cửa):** `["mèo","chó","mèo","chim"]` → mèo(mới,giữ) · chó(mới,giữ) ·
  mèo(đã có,bỏ) · chim(mới,giữ) → `["mèo","chó","chim"]`, giữ đúng thứ tự lần đầu xuất hiện.

- **CTDLGT bên trong:** hash set → kiểm tra `in` là **O(1)**, tổng **O(n)**. Nếu dùng `list`
  (`in` là O(n)) thì tổng thành **O(n²)** — đây là lý do phải chọn đúng cấu trúc dữ liệu.

- **Bẫy dễ sai:** (1) `seen = set` thiếu `()` → TypeError; (2) chỉ `seen.add` mà quên
  `result.append` → trả về list rỗng. Xem [bug-log](./bug-log.md) #2, #3.



### Edit distance / Levenshtein (DP) · Phase 0 · 2026-07-16

- **Bài toán nó giải:** hash **không đủ** cho near-dup — chunk chỉ thừa 1 dấu chấm là hash đổi
  hoàn toàn, 2 câu gần y nhau bị coi là khác → vẫn embed cả 2, tốn tiền + nhiễu top-k.
  Cần chuyển từ hỏi "giống hệt không?" (hash) sang đo "**khác bao nhiêu?**" (distance).

- **Công thức / thuật toán:** dựng lưới `(len(A)+1) × (len(B)+1)`; ô `(i,j)` = distance giữa
  i ký tự đầu của A và j ký tự đầu của B. Ba bước:
  1. **Viền:** hàng đầu `0,1,2,…` (thêm j lần) · cột đầu `0,1,2,…` (xoá i lần).
  2. **Mỗi ô trong = min của 3 đường** (nhớ **luôn cộng phí**):
     ```
     trên  = giá_trị_trên  + 1        (xoá)
     trái  = giá_trị_trái  + 1        (thêm)
     chéo  = giá_trị_chéo  + cost     (cost = 0 nếu 2 ký tự GIỐNG, = 1 nếu KHÁC)
     ô     = min(trên, trái, chéo)
     ```
  3. **Đáp án = ô góc dưới-phải.** (Phải điền CẢ lưới — đường rẻ nhất tự bẻ ngang/xuống/chéo,
     không nhẩm mỗi đường chéo được.)

- **Ví dụ bằng SỐ THẬT:** A="beo" (hàng) vs B="meo" (cột) → distance = 1 (thay b↔m):
  ```
        ""  m  e  o
    ""   0  1  2  3
    b    1  1  2  3
    e    2  2  1  2
    o    3  3  2  1   ← ô cuối = 1
  ```
  Đường rẻ nhất: tốn 1 tại `b≠m`, rồi `e=e`, `o=o` đi chéo miễn phí bê số 1 về đích.
  Các kiểu khác: xoá (`meo/eo`=1, đường bẻ XUỐNG) · thêm (`cat/cats`=1, bẻ NGANG) ·
  khác hết (`cat/dog`=3, chéo nhưng +1 mỗi bước).

- **CTDLGT bên trong:** DP + lưới 2 chiều (list lồng list). Độ phức tạp **O(n·m)** một cặp.
  Near-dup ngây thơ so mọi cặp chunk → O(số_chunk² × độ_dài²) → scale lớn phải normalize+hash
  trước rồi MinHash, edit distance chỉ cho chunk ngắn/ít.

- **Bẫy dễ sai:** (1) **quên +1** khi cộng phí đường đi (dính 3 lần! — xem [bug-log](./bug-log.md) #4);
  (2) tưởng "chỉ cần dò đường chéo chính là ra đáp án" — sai, phải điền cả lưới lấy ô cuối;
  (3) `grid[n,m]` sai cú pháp — lưới 2 chiều truy cập bằng `grid[i][j]`, ô cuối là `[n-1][m-1]` (#5);
  (4) `[[0]*n]*m` tạo m hàng **trỏ chung 1 hàng** — sửa 1 ô, cả cột đổi theo.

- **Khi nào đáng bật (flag):** bản tay = để hiểu + debug. Production: **normalize + hash exact**
  trước (bắt 90% ca vặt, O(1)) → còn lại `rapidfuzz` (C, nhanh) hoặc **MinHash** khi scale.
  Cắm thư viện vào **cuối Phase 0** theo quy ước, flag mặc định TẮT, ngưỡng chọn bằng eval (Phase 3).


### Incremental ingest · Phase 0 · 2026-07-17

- **Bài toán nó giải:**
    Idempotent — chạy lại pipeline bao nhiêu lần cũng không bị dup dữ liệu. `dedup_exact` và
    near-dup (edit distance) chỉ check trùng **trong 1 lần gọi**, không nhớ được giữa các lần chạy.

- **Công thức / thuật toán:**
    Load `seen` (tập hash) từ file — nếu chưa có file thì `seen` rỗng. Với mỗi chunk mới: tính
    hash, nếu đã có trong `seen` thì bỏ qua, chưa có thì embed/save và thêm hash đó vào `seen`.
    …

- **Ví dụ bằng SỐ THẬT:** …
ví dụ "mèo, gà, chó " trong lượt đầu lượt hai là "mèo , gà, chó , chim " check tại vì mèo gà chó đã có trong seen rồi nên chỉ cần insert cái hash của chim

- **CTDLGT bên trong:** … (hash map? heap? graph?) + độ phức tạp O(?)
  cấu trúc dữ liệu bên trong là hash set (chỉ cần biết có/không, không cần key→value), độ phức tạp O(n)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  - **Bẫy dễ sai:** định nghĩa `save_seen()` xong **quên gọi nó** trong `incremental_ingest` —
  `seen.add()` chỉ sửa object trong RAM, không tự ghi xuống file. Không crash, chỉ khiến lần
  chạy sau coi mọi thứ là mới. Test 1-lần-gọi không bắt được, phải test 2 lần liên tiếp mới lộ.
  Xem [bug-log](./bug-log.md) #7.

- **Khi nào đáng bật (flag):** gần như luôn bật — khác với semantic/proposition chunking (nâng
  *chất lượng*, tuỳ chọn), incremental ingest giải quyết *chi phí + idempotency*, cần thiết bất
  cứ khi nào ingest chạy lặp lại trên cùng nguồn. Chỉ bỏ qua nếu chắc chắn pipeline **chỉ chạy
  đúng 1 lần, không bao giờ lặp lại** trên cùng dữ liệu.



### Cosine similarity · Phase 1 · 2026-07-19

- **Bài toán nó giải:** sau khi có vector cho mỗi đoạn text (embedding), cần 1 con số đo
  "2 đoạn giống nhau bao nhiêu" để tìm chunk liên quan tới câu hỏi — đo bằng **góc** giữa 2
  vector, bỏ qua độ dài.

- **Công thức / thuật toán:** `cos(a,b) = (a·b) / (||a|| × ||b||)`.
  `dot = a·b` = tổng nhân từng cặp phần tử tương ứng. `||v||` = căn bậc 2 tổng bình phương từng
  phần tử của vector đó.

- **Ví dụ bằng SỐ THẬT:**
  ```
  a = [1, 0], b = [1, 1]
  dot(a,b) = 1*1 + 0*1 = 1
  ||a|| = √(1²+0²) = 1
  ||b|| = √(1²+1²) = √2 ≈ 1.414
  cos(a,b) = 1 / (1 × 1.414) ≈ 0.707   (góc 45°)
  ```
  Test thật với vector từ `BAAI/bge-m3`:
  ```
  cos("xin chào", "hello")    = 0.854   ← rất giống, dù khác ngôn ngữ hoàn toàn
  cos("xin chào", "con mèo")  = 0.618   ← thấp hơn hẳn, nghĩa khác
  ```

- **CTDLGT bên trong:** thuần toán (dot product + norm), không cấu trúc dữ liệu đặc biệt.
  Độ phức tạp **O(d)** với d = số chiều vector (1024 với bge-m3).

- **Bẫy dễ sai:** nhầm `+` với `*` ở mẫu số (xem [bug-log](./bug-log.md) #8) — **và** bẫy nặng
  hơn: khi thấy test đỏ, sửa **đáp án trong test** cho khớp code sai, thay vì sửa code (#9).

- **Khi nào đáng bật (flag):** luôn dùng — đây là phép đo lõi của mọi retrieval dựa trên
  vector, không phải kỹ thuật tuỳ chọn.

---

### Embedder & VectorStore Port (hexagonal architecture) · Phase 1 · 2026-07-19

- **Bài toán nó giải:** `domain`/`application` không được phụ thuộc trực tiếp vào thư viện cụ
  thể (`FlagEmbedding`, `qdrant-client`) — đổi model/kho vector sau này, code gọi nó **không
  cần sửa gì**.

- **Công thức / thuật toán:** dùng `typing.Protocol` khai báo "hợp đồng" (interface) — chỉ có
  chữ ký hàm (thân là `...`), không logic thật. `Embedder` cần `dim: int` +
  `embed(texts: list[str]) -> list[list[float]]` (chú ý: **batch**, không phải 1 câu 1 lần).
  `VectorStore` cần `SearchHit` (dataclass `id/text/score`) + `upsert`/`search` đều **bắt buộc**
  tham số `tenant_id`.

- **Ví dụ:** class nào có đúng field/method khớp Protocol thì tự động "hợp lệ" — không cần
  khai báo kế thừa tường minh (`class Foo(Embedder)` không bắt buộc, chỉ cần đúng hình dạng).

- **CTDLGT bên trong:** không phải CTDLGT truyền thống — đây là mẫu thiết kế **Port/Adapter**
  (Hexagonal Architecture): Port = giao diện thuần domain, Adapter = implementation thật gọi
  thư viện ngoài.

- **Bẫy dễ sai:** nhầm `__init__.py` (file đánh dấu package, phải rỗng) với `__init__` (hàm
  khởi tạo bên trong class) — dán nhầm code vào file package khiến class thật thiếu mất phần
  quan trọng; quên `self` ở method; nhét thuộc tính (`dim`) vào trong ngoặc của method thay vì
  khai báo riêng 1 dòng độc lập.

- **Khi nào đáng bật (flag):** luôn dùng khi có tầng infrastructure gọi thư viện ngoài —
  nguyên tắc gốc hexagonal của dự án, không phải optional.

---

### BGEEmbedder (BAAI/bge-m3) · Phase 1 · 2026-07-19

- **Bài toán nó giải:** cần 1 embedder **thật** (không phải giả lập) sinh vector 1024 chiều đa
  ngôn ngữ từ text, implement đúng Protocol `Embedder`.

- **Công thức / thuật toán:** load model 1 lần trong `__init__`
  (`self.model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=False)`, `self.dim = 1024`);
  `embed()` gọi `self.model.encode(texts)['dense_vecs'].tolist()` — `encode` xử lý theo
  **batch** (nhiều câu 1 lần, nhanh hơn hẳn gọi từng câu lẻ).

- **Ví dụ bằng SỐ THẬT:** `embed(["xin chào", "hello", "con mèo"])` → 3 vector, mỗi vector dài
  1024. Ghép với `cosine_similarity` (mục trên) → chứng minh model hiểu **NGHĨA** xuyên ngôn
  ngữ, không so chữ.

- **CTDLGT bên trong:** mạng neural transformer đã train sẵn (KHÔNG tự code lại được — cần dữ
  liệu khổng lồ + GPU cluster). Phần tự code tay được là toán xử lý **output** của nó (cosine
  similarity ở trên).

- **Bẫy dễ sai:** tạo model xong quên gán `self.model = ...` (model bị tạo ra rồi biến mất);
  `.toList()` sai case (đúng là `.tolist()`, chữ thường); cắt `[0]` làm mất kết quả batch, chỉ
  giữ đúng 1 vector; chạy nhầm `python3` hệ thống thay vì `.venv/bin/python3` →
  `ModuleNotFoundError` dù thư viện đã cài đúng chỗ.

- **Khi nào đáng bật (flag):** cắm thay embedder giả khi cần chạy thật/tích hợp Qdrant; giữ
  1 fake embedder riêng cho unit test nhanh, không cần load model thật (~vài giây mỗi lần).

---

### QdrantStore + Tenant Isolation + UUID5 · Phase 1 · 2026-07-19

- **Bài toán nó giải:** lưu vector đã embed vào kho thật (Qdrant) để tìm lại sau. Nhiều tenant
  (niche/khách hàng khác nhau) **share chung 1 collection** — quên lọc đúng tenant lúc `search`
  (chưa code, để buổi sau) là **silent failure**: không crash, chỉ âm thầm rò dữ liệu tenant
  khác.

- **Công thức / thuật toán:**
  - `_ensure_collection`: kiểm tra `collection_exists` **trước** khi `create_collection` —
    idempotent, gọi lại nhiều lần không lỗi.
  - `upsert`: dùng `zip(ids, texts, vectors)` gộp 3 danh sách song song thành list
    `PointStruct(id, vector, payload={tenant_id, text})`.
  - `id` gốc được băm qua `uuid.uuid5(uuid.NAMESPACE_DNS, id_gốc)` trước khi gán — vì (a)
    Qdrant chỉ chấp nhận id dạng số nguyên hoặc UUID, không nhận string tuỳ ý; và (b) idempotent
    — cùng id gốc luôn ra cùng UUID, ingest lại **ghi đè** thay vì tạo bản trùng.

- **Ví dụ bằng SỐ THẬT:** `upsert('tenant_a', ['1'], ['xin chào'], [vector])` gọi 2 lần liên
  tiếp (cùng id gốc `"1"`) đều thành công, không tạo điểm thứ 2 — vì `uuid5("1")` luôn ra đúng
  1 UUID cố định.

- **CTDLGT bên trong:** vector database có index tìm gần đúng (HNSW bên trong Qdrant, chưa cần
  hiểu sâu ở Phase 1) + hash 1 chiều (`uuid5` = hash namespace+name → UUID cố định).

- **Bẫy dễ sai:** thân `if not collection_exists(...):` bị thụt lề sai khiến `create_collection`
  luôn chạy dù có điều kiện bọc ngoài (#10, không lỗi cú pháp — sai Ý NGHĨA logic); đổi tên biến
  vòng lặp (`id_`→`id`) nhưng quên sửa chỗ dùng (#11); Qdrant point id không nhận string tuỳ ý,
  phải số nguyên hoặc UUID (#12).

- **Khi nào đáng bật (flag):** luôn dùng — đây là adapter lõi của Phase 1. Tenant filter ở
  `search` (buổi sau) là **bắt buộc tuyệt đối**, không phải flag tuỳ chọn.


### BM25 (sparse retrieval) · Phase 2 · 2026-07-__   ⟵ KHUNG, điền sau khi code

- **Bài toán nó giải:** _(điền: dense/vector thua ở đâu? mã sản phẩm/tên riêng/từ hiếm →
  vì sao cần so từ khoá thẳng?)_

- **Công thức / thuật toán:**
  ```
                      TF × (k1 + 1)
  score = IDF  ×  ─────────────────────────────────
                   TF + k1 × (1 - b + b × dl/avgdl)

  IDF(t) = log( (N - df + 0.5) / (df + 0.5) + 1 )
  k1 = 1.5 (tốc độ TF chững / saturation)   ·   b = 0.75 (mức phạt độ dài)
  ```
  3 viên gạch: **TF saturation** (TF ở cả tử+mẫu → chững, `k1` chỉnh) · **IDF** (từ hiếm→cao) ·
  **length norm** (`dl/avgdl` ở mẫu → phạt doc dài, `b` chỉnh). _(diễn giải lại bằng lời mình)_

- **Ví dụ bằng SỐ THẬT:** _(điền sau khi code: dựng inverted index cho 2-3 doc, tính điểm 1 query
  bằng tay rồi so với hàm. Nhớ ca `dl/avgdl=1` → cụm length = 1, không phạt.)_

- **CTDLGT bên trong:** **Inverted index** = hash map `term → [doc ids]`, tra O(1) thay vì
  quét mọi doc O(n). _(bổ sung độ phức tạp tổng khi code xong)_

- **Bẫy dễ sai:** _(để trống — điền bug gặp khi code: quên +0.5 trong IDF? nhầm TF với DF?
  quên chia avgdl? …)_

- **Khi nào đáng bật (flag):** _(điền: sparse mạnh cho keyword/mã; kết hợp dense qua hybrid;
  production cắm rank-bm25 cuối phase)_