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
