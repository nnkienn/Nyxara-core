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


### BM25 (sparse retrieval) · Phase 2 · 2026-08-02

- **Bài toán nó giải:** dense/embedding (cosine, Phase 1) hiểu **nghĩa** nhưng yếu ở khớp
  **từ khoá chính xác** — mã sản phẩm, tên riêng, từ hiếm. BM25 là tìm kiếm **lexical**
  (so chữ trùng nhau, không phải "ngữ nghĩa") — bù đúng chỗ dense yếu. Vì 2 cái bổ sung
  nhau nên hybrid (Phase 2.1 tiếp theo) mới cần dùng cả hai.

- **Công thức / thuật toán:**
  ```
                      TF × (k1 + 1)
  score = IDF  ×  ─────────────────────────────────
                   TF + k1 × (1 - b + b × dl/avgdl)

  IDF(t) = log( (N - df + 0.5) / (df + 0.5) + 1 )
  k1 = 1.5 (tốc độ TF chững / saturation)   ·   b = 0.75 (mức phạt độ dài)
  ```
  2 trụ cốt lõi: **IDF** — từ càng hiếm (`df` nhỏ so với `N`) càng quan trọng, **cố định**
  cho 1 term, không đổi theo từng doc. **Length normalization** (`dl/avgdl`) — cùng 1 lần
  xuất hiện, doc càng **ngắn** thì tín hiệu càng **mạnh** (từ đó chiếm tỉ trọng lớn hơn của
  cả doc); `dl/avgdl=1` (doc dài đúng mức trung bình) → không phạt không thưởng.

- **Ví dụ bằng SỐ THẬT:** 3 doc tenant `t1`: `doc1="con mèo đen"`, `doc2="con chó nâu"`,
  `doc3="mèo và chó"` (mỗi doc 3 từ, `avgdl=3`). Inverted index: `"mèo": {doc1:1, doc3:1}`
  (df=2), `"đen": {doc1:1}` (df=1). Query `"mèo đen"`:
  ```
  IDF("mèo") = log((3-2+0.5)/(2+0.5)+1) = log(1.6)   ≈ 0.470
  IDF("đen") = log((3-1+0.5)/(1+0.5)+1) = log(2.667)  ≈ 0.981
  score(doc1) = 0.470 + 0.981 ≈ 1.451   (chứa cả "mèo" và "đen")
  score(doc3) = 0.470                    (chỉ chứa "mèo")
  score(doc2) = không tính — không chứa từ nào trong query
  ```
  Chạy code thật ra đúng `1.4508` / `0.4700` — khớp tay 100%.

- **CTDLGT bên trong:** **Inverted index** = hash map lồng
  `tenant_id → term → {doc_id: term_freq}`, tra `df`/`tf` O(1) thay vì quét mọi doc O(n).
  `search` gộp candidate doc qua các term rồi `sorted(..., reverse=True)[:top_k]` — sort
  O(n log n) trên tập candidate, không phải toàn bộ corpus.

- **Bẫy dễ sai:**
  1. **Nhầm IDF với length norm** — tưởng doc dài hơn thì từ "hiếm hơn" nên điểm cao hơn.
     Sai: IDF không đổi theo doc (tính trên toàn corpus), chỉ có mẫu số (`dl/avgdl`) mới
     quyết định ai cao ai thấp giữa các doc — doc **ngắn** mới điểm cao hơn ở TF ngang nhau.
  2. **`avgdl` không phải độ dài doc đang chấm** — là độ dài **trung bình toàn tenant**; nếu
     tất cả doc ví dụ cùng độ dài thì `dl/avgdl` luôn =1, che mất tác dụng thật của length
     norm (dễ ngộ nhận nó "không làm gì" — phải test với doc độ dài khác nhau mới thấy).
  3. **`IndentationError`** — thân vòng `for term, tf in freq.items():` viết thẳng hàng với
     `for` thay vì thụt lề thêm 1 cấp → Python báo lỗi ngay khi chạy (lỗi cú pháp, chạy là
     bắt được, không cần đọc kỹ).
  4. **Quên xử lý `tf=0`** (term không có trong doc) — phải trả `0.0` sớm trong `_score`,
     không được để rơi xuống tính `log`/chia cho 0 hoặc cộng nhầm điểm không tồn tại.

- **Khi nào đáng bật (flag):** luôn bật song song với dense trong Hybrid — sparse mạnh
  cho keyword/mã sản phẩm/tên riêng mà dense bỏ sót. Bản tay dùng để hiểu + debug; production
  cắm `rank-bm25` hoặc `bm25s` cuối Phase 2.1, so kết quả với bản tay trước khi thay hẳn.

---

### RRF — Reciprocal Rank Fusion · Phase 2 · 2026-08-02

- **Bài toán nó giải:** dense (cosine, 0–1) và BM25 (không giới hạn) khác đơn vị, không cộng
  thẳng điểm gốc được. RRF né vấn đề đó bằng cách **chỉ nhìn thứ hạng** (rank) của doc trong
  từng danh sách, không nhìn điểm số gốc — rank thì luôn so sánh được dù nguồn nào tạo ra nó.

- **Công thức / thuật toán:**
  ```
  RRF(d) = Σ 1/(k + rank_i(d))    k=60 (Cormack 2009)
  ```
  Cộng theo rank (không phải điểm) vì rank là đại lượng chung, không lệ thuộc đơn vị của từng
  nguồn. Doc đứng hạng cao ở **cả 2** danh sách được cộng lớn ở cả 2 lần → tổng cao nhất — ưu
  tiên "ổn định ở nhiều nguồn" hơn "xuất sắc 1 nguồn, tệ nguồn kia". `k=60` là hằng số làm mượt
  (smoothing) lấy từ thực nghiệm — không cần tune theo dataset, đây là lý do RRF phổ biến.

- **Ví dụ bằng SỐ THẬT:** 3 doc, 2 danh sách hạng khác nhau có chủ đích:
  ```
  dense_ranked = ["doc2", "doc1", "doc3"]   # hạng: doc2=1, doc1=2, doc3=3
  bm25_ranked  = ["doc1", "doc3", "doc2"]   # hạng: doc1=1, doc3=2, doc2=3

  RRF(doc1) = 1/61 + 1/62 ≈ 0.032522   (hạng 2, hạng 1 — đều tay ở cả 2)
  RRF(doc2) = 1/61 + 1/63 ≈ 0.032266   (hạng 1, hạng 3 — mạnh 1 bên, yếu bên kia)
  RRF(doc3) = 1/62 + 1/63 ≈ 0.032002   (hạng 3, hạng 2)
  ```
  Chạy code thật ra đúng `0.03252247 / 0.03226646 / 0.03200205` — khớp tay. Xếp hạng cuối
  `doc1 > doc2 > doc3`, dù `doc2` từng đứng **#1 tuyệt đối** ở dense vẫn thua `doc1` vì không
  ổn định ở cả 2 nguồn — đúng hành vi RRF được thiết kế để tạo ra.

- **CTDLGT bên trong:** **Merge N ranked list** qua hash map trung gian — `enumerate(list,
  start=1)` lấy rank O(n) mỗi danh sách, cộng dồn vào dict O(1)/lần, tổng O(Σ len(list)); sort
  cuối O(m log m) với m = số doc duy nhất xuất hiện ở ít nhất 1 danh sách.

- **Bẫy dễ sai:**
  1. **`enumerate(list)` mặc định bắt đầu từ 0**, phải truyền `start=1` — nếu quên, mọi rank
     lệch đi 1, kéo theo mọi `1/(k+rank)` sai (dù sai lệch nhỏ vì `k=60` che bớt, vẫn là bug).
  2. Doc chỉ xuất hiện ở **1 trong 2** danh sách thì **chỉ cộng phần có**, không tự bịa rank
     cho danh sách còn thiếu (không có nghĩa là rank=cuối bảng hay rank=0).
  3. **Cú pháp `int | None` cần Python 3.10+** — dự án chạy Python 3.9.6, dùng `Optional[int]`
     (từ `typing`) thay vì `|` để union type hoạt động đúng version hiện tại.
  4. **Thụt lề sai 2 lần liên tiếp** khi gõ lại: (a) để sót `raise NotImplementedError` của
     khung phía trên code thật → code thật không bao giờ chạy tới; (b) toàn khối bị thụt lề
     nhiều hơn dòng trước nó dù dòng trước không mở khối (`IndentationError: unexpected
     indent`) — xem [bug-log](./bug-log.md) #15, #16.

- **Khi nào đáng bật (flag):** luôn bật khi dùng Hybrid — đây chính là bước hợp nhất dense +
  BM25 thành 1 danh sách duy nhất để đưa vào cross-encoder rerank (Phase 2.2). Bản thân điểm
  RRF không có ý nghĩa tuyệt đối, chỉ dùng để sort/chọn top_k ứng viên — sẽ bị thay hoàn toàn
  bởi điểm cross-encoder ở bước sau.

---

### Cross-encoder Reranking (bge-reranker-v2-m3) · Phase 2 · 2026-08-03

- **Bài toán nó giải:** bi-encoder (dense, Phase 1) encode query và doc **riêng biệt** rồi so
  vector — nhanh (pre-compute được) nhưng mất chi tiết vì đã "nén" mỗi bên độc lập trước khi
  so. Cross-encoder đọc `(query, doc)` **cùng lúc** trong 1 forward-pass → model có thể chú ý
  qua lại giữa từng từ 2 bên → chính xác hơn hẳn, nhưng không pre-compute được (chưa biết query
  lúc index) → phải chạy lại cho từng cặp, chậm hơn nhiều. Vì vậy chỉ chạy trên tập nhỏ đã lọc
  sẵn bởi HybridRetriever (Phase 2.1), không chạy trên toàn kho.

- **Công thức / thuật toán:** không có công thức tay — bản thân model (transformer) đã train
  sẵn, phần code tay được chỉ là **cách gọi đúng API**: `compute_score([[query, doc], ...])`
  nhận list các cặp, trả về **list điểm số tương ứng, cùng thứ tự**. Điểm **không giới hạn
  0-1** (logit thô) trừ khi bật `normalize=True` lúc khởi tạo model.

- **Ví dụ bằng SỐ THẬT:** `score("mèo đen", ["con mèo màu đen dễ thương", "con chó màu nâu"])`
  → `[4.75, -2.07]` — đoạn liên quan ra điểm dương cao, đoạn không liên quan ra điểm **âm**.
  Khác hẳn BM25 (luôn ≥0) hay cosine (luôn trong [-1,1]) — một lý do nữa vì sao không thể trộn
  điểm cross-encoder thẳng với điểm nguồn khác mà không cân nhắc.

- **CTDLGT bên trong:** không phải CTDLGT cổ điển — giống Embedder (Phase 1), là mạng
  transformer đã train sẵn, phần tự code chỉ là **Port/Adapter** (hexagonal, giống
  `Embedder`/`VectorStore`): `Reranker` Protocol chỉ có `score(query, docs) -> list[float]`.

- **Bẫy dễ sai:** `HybridRetriever.search()` chỉ trả `(doc_id, score)`, **không có text** —
  doc chỉ khớp qua BM25 (không qua dense) thì chưa từng có text lưu lại ở đâu cả (BM25Index
  không lưu text, chỉ lưu tần suất từ). Muốn rerank cần text thật của từng candidate — đây là
  **lỗ hổng kiến trúc chưa giải quyết**, không phải bug, cần thêm cơ chế `doc_id → text` trước
  khi ghép cross-encoder vào cuối pipeline thật.

- **Khi nào đáng bật (flag):** luôn bật sau Hybrid khi cần độ chính xác cao cho top kết quả
  cuối cùng (ví dụ nội dung đưa cho bác sĩ/bệnh nhân) — chi phí chỉ trả cho ~30-50 ứng viên đã
  lọc, không phải toàn kho.

---

### CRAG (Corrective RAG) — State Machine · Phase 2 · 2026-08-12

- **Bài toán nó giải:** pipeline retrieval (Hybrid+Rerank) không đảm bảo kết quả tìm được luôn
  **đủ tốt** — câu hỏi lạ, kho thiếu dữ liệu, rerank vẫn chọn nhầm. Nếu cứ đưa thẳng cho LLM
  sinh câu trả lời mà không kiểm tra, dễ ra ảo giác (trả lời tự tin từ context sai). CRAG thêm
  1 bước "giám khảo" kiểm tra chất lượng context **trước khi** cho generate, và **tự sửa** (tìm
  lại rộng hơn) nếu context tệ — thay vì chạy thẳng 1 đường như Phase 2.1/2.2.

- **Công thức / thuật toán:** không phải công thức toán — là 1 **đồ thị trạng thái** (state
  machine), gồm 3 khái niệm:
  ```
  state  = 1 dict mang dữ liệu chạy xuyên suốt (query, retrieved_docs, verdict, attempts, answer...)
  node   = 1 hàm (state) -> dict cập nhật một phần state (retrieve/grade/generate)
  edge   = đường nối 2 node. "Edge thường" luôn đi 1 hướng cố định.
           "Conditional edge" đọc state rồi TỰ CHỌN node kế tiếp (dùng cho rẽ nhánh CORRECT/INCORRECT).
  ```
  Luồng: `retrieve → grade → (INCORRECT & attempts<max: quay lại retrieve) | (còn lại: generate) → END`.
  `grade` tự đếm CÓ/KHÔNG từng doc (`decide()`, ngưỡng `>=0.6`→CORRECT, `<=0.0`→INCORRECT,
  còn lại→AMBIGUOUS — ngưỡng là **tham số**, không phải chân lý toán học, tự chọn hợp lý rồi để
  Phase 3 (eval) kiểm chứng thật, giống cách chọn `k1/b` của BM25 hay `k=60` của RRF).

- **Ví dụ bằng SỐ THẬT:** verify bằng graph thật, 2 kịch bản đối lập:
  ```
  Grader luôn trả lời "liên quan" (True):
    → retrieve → grade (verdict=CORRECT, attempts=1) → generate → END
    → answer có ngay, KHÔNG lặp.

  Grader luôn trả lời "không liên quan" (False), max_attempts=3:
    → retrieve→grade (INCORRECT, attempts=1) → retrieve→grade (INCORRECT, attempts=2)
    → retrieve→grade (INCORRECT, attempts=3) → attempts>=max nên VẪN generate (van an toàn)
    → answer vẫn có, verdict cuối cùng vẫn "INCORRECT" (không giả vờ là đúng, chỉ là buộc dừng).
  ```

- **CTDLGT bên trong:** **Graph** (node/edge, conditional routing) + **cycle guard** (`attempts`
  chặn lặp vô hạn — cùng họ với recursion base-case, DFS visited-set). Mỗi node là 1 **closure**
  (hàm ngoài nhận dependency đã inject — `retriever`, `grader`... — trả về hàm trong chỉ nhận
  đúng `state`, "nhớ" dependency đó dù hàm ngoài đã chạy xong) — LangGraph chỉ chấp nhận node
  dạng `(state) -> dict`, không truyền thêm tham số nào khác được.

- **Bẫy dễ sai:**
  1. **Conditional edge (router) không được sửa `state`** — nó chỉ được trả về 1 string chọn
     node kế tiếp. Việc `attempts += 1` phải nằm trong 1 **node thật** (ở đây gộp vào
     `grade_node`, vì mỗi lần `grade` chạy = vừa thử thêm 1 lần), không thể đặt trong `route()`.
  2. Quên khai báo field mới (`grades`, `tenant_id`) trong `state.py` (`TypedDict`) trước khi 1
     node trả về key đó — không lỗi cú pháp, chỉ là state "không đồng bộ" giữa các node.
  3. `httpx.post` timeout mặc định quá ngắn cho LLM; `.upper()` 1 bên mà quên chuẩn hoá bên so
     sánh — xem [bug-log](./bug-log.md) `#18`, `#19`.

- **Khi nào đáng bật (flag):** luôn bật khi RAG phục vụ nội dung có rủi ro sai (y tế, tài
  chính...) — chi phí thêm 1 lượt LLM chấm điểm, đổi lại giảm hẳn nguy cơ trả lời từ context
  rác. Với nội dung ít rủi ro, có thể tắt để giảm độ trễ + chi phí gọi LLM.