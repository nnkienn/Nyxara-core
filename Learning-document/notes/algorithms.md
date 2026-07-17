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