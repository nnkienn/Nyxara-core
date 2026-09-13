# 🚩 TRẠM 5 — Recursive chunking (soạn 2026-09-13 tối, để trace sáng 14/09)

> **Cách dùng:** mở kèm [`app/application/chunking/recursive_chunker.py`](../../../app/application/chunking/recursive_chunker.py)
> và [`app/presentation/api/ingest.py`](../../../app/presentation/api/ingest.py).
> **Đọc THÂN HÀM, đừng tin tên hàm, đừng tin bản tóm tắt bên dưới.**
> File này **không có đáp án** — đúng luật [§3.5](../../../CLAUDE.md). Bài đo nào cần chạy thì bảo Claude chạy hộ,
> user chỉ **dự đoán trước** rồi đọc số (luật 09/09).
>
> 🖥️ Sáng mai học ở công ty (máy Fedora) → **`git pull` trước khi mở**, tối 13/09 có 3 commit mới.

---

## ⚠️ Bản tóm tắt dưới đây CÓ ÍT NHẤT 4 CHỖ SAI — tìm ra từng chỗ, sửa bằng lời của bạn

> *"`/ingest` nhận `text` rồi gọi `recursive_chunk(text, chunk_size, chunk_overlap)`. Hàm này dùng
> `re.split`, mà `re.split` thì luôn giữ lại dấu tách, nên không mất ký tự nào. Nó cắt sạch mọi dấu
> tách trong danh sách `separators` ngay trong một lượt, rồi `merge_pieces` gộp các mẩu lại và đảm
> bảo mọi chunk đều ngắn hơn hoặc bằng `size`. Cuối cùng `/ingest` trả `chunk_count` = số chunk đã
> ghi vào cả 3 kho."*

Với **mỗi** chỗ sai: (a) chỉ ra câu sai · (b) trích **nguyên văn dòng code** chứng minh nó sai ·
(c) viết lại câu đó cho đúng.

---

## Trạm 5a — `re.split` và cặp ngoặc

```python
text = "Cau mot. Cau hai."
sep  = "."
```

Điền bảng (chưa chạy, dự đoán trước):

| Biểu thức | Bạn dự đoán kết quả |
|---|---|
| `text.split(sep)` | |
| `re.split(re.escape(sep), text)` | |
| `re.split("(" + re.escape(sep) + ")", text)` | |
| `"".join(...)` của dòng 1 có `== text` không? | |
| `"".join(...)` của dòng 3 có `== text` không? | |

**🔨 Việc làm bằng tay:** trong file, `mau` được dựng bằng `"(" + re.escape(sep) + ")"`.
Bỏ `re.escape` đi thì với `sep = "."` chuyện gì xảy ra, và **vì sao**? Trả lời trước, rồi nhờ Claude chạy để đối chiếu.

---

## Trạm 5b — vòng lặp dán dấu tách (chỗ có 2 điều kiện mới thêm tối 13/09)

```python
text = " mo dau"        # CHÚ Ý: mở đầu bằng một khoảng trắng
sep  = " "
```

Điền từng vòng — cột `chốt?` phải trả lời **dựa trên điều kiện thật trong code**, không dựa trên cảm giác:

| vòng | `part` | `temp` sau khi gom | chốt? vì sao | `ghep` |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |
| *hết vòng lặp* | — | | | |

**🔨 Việc làm bằng tay (đây là bài đóng-sách 10' đã hẹn):** đóng file, tự viết lại **2 điều kiện**:
① điều kiện chốt `temp` khi gặp dấu tách · ② cách xử lý phần sót cuối khi nó không có chữ.
Viết ra editor trống rồi mới mở file so.

**Câu chốt:** bỏ chữ `.strip()` ở điều kiện ① thì test nào trong
[`test_recursive_chunker.py`](../../../tests/application/chunking/test_recursive_chunker.py) đỏ, và nó đỏ ở **ca nào**?

---

## Trạm 5c — đệ quy: mỗi tầng rụng một dấu tách

```python
split_by_separators("Meo thich ngu\n\nCho thich chay", size=10, separators=["\n\n", " "])
```

| Tầng | `text` đang xử lý | `sep` | `separators` truyền xuống tầng dưới | mẩu nào phải đi tiếp xuống? vì sao |
|---|---|---|---|---|
| ngoài cùng | | | | |
| tầng 2 | | | | |
| tầng 3 | | | | |

**Hai câu phải trả lời bằng dòng code, không bằng trí nhớ:**
1. Điều kiện nào làm đệ quy **dừng**? (có 2 vế — chỉ ra cả hai)
2. Mẩu nào được `append` thẳng, mẩu nào đi qua `extend`? Khác nhau chỗ nào — và nếu đảo hai cái đó thì
   kết quả trông thế nào? *(gợi ý: bạn đã đoán sai đúng cặp này trong drill tối 13/09)*

**🔨 Việc làm bằng tay:** dự đoán **đầy đủ** list kết quả của lệnh trên, viết ra, rồi nhờ Claude chạy đối chiếu.

---

## Trạm 5d — nối vào `/ingest`: hợp đồng giữa hai tầng

Mở [`ingest.py`](../../../app/presentation/api/ingest.py), đọc thân `ingest()`.

| Câu hỏi | Trả lời + dòng code chứng minh |
|---|---|
| `chunk_count` trong response đếm **cái gì**? | |
| `payload.chunk_overlap` đi tới đâu? | |
| Nếu client gửi `chunk_overlap=50`, kết quả khác gì so với `chunk_overlap=0`? | |
| Bug số mấy đang ghi đúng chuyện này? | |

**Câu thiết kế (C2 — mốc sắp tới, nghĩ trước để mai bàn):** muốn trả về được **vị trí đầu/cuối** của mỗi chunk
trong văn bản gốc thì kiểu trả về của `recursive_chunk` phải đổi.
1. Đổi `list[str]` → chunk có kèm offset là **additive hay breaking**? Tiêu chí phân biệt là gì?
2. **Ai** sẽ gãy? (kể tên file thật trong repo, không nói chung chung)
3. Vì sao C1 (giữ separator) **bắt buộc phải xong trước** C2? *(gợi ý: thử tính offset trên phiên bản `str.split` nuốt dấu tách)*

---

## Chốt trạm (không được bỏ)

1. Viết **một dòng assert** diễn tả lời hứa lõi nhất của chunker này. Vì sao nó mạnh hơn
   `assert result == [...]` của một ca cụ thể?
2. `CHUNK > size` xuất hiện khi `size=3` — **bug hay đúng thiết kế**? Trả lời kèm lý do, và nói xem
   quyết định đó là của ai, ngày nào.
3. Tự sửa mọi chỗ sai bạn tìm được ở đầu file **bằng lời của mình** (không copy câu của Claude),
   rồi ghi bug mới (nếu có) vào [bug-log.md](../bug-log.md).
