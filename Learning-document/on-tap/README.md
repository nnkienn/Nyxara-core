# 📇 Thẻ ôn — mỗi kỹ thuật một thẻ

Mỗi thẻ giống hệt nhau về khuôn, nên ôn thẻ nào cũng làm cùng một cách.
**Mọi con số trong thẻ được chạy ra từ code thật trong `app/`** (17/10/2026), không phải số chép tay.

## Ôn một thẻ — 4 bước, ~15 phút

1. **Đọc mục 1–2** (bài toán + kiến thức) — 2'. Chỉ đọc, chưa làm gì.
2. **Che mục 3, tự tính ví dụ ra giấy** — 5'. Xong mới mở mục 3 so từng số.
3. **Mục 6 "Tự kiểm"** — đóng sách, trả lời **thành tiếng** câu phỏng vấn + làm bài tính, **rồi mới** bấm ▶ mở đáp án.
4. **Chấm** ✅ trôi chảy · ⚠️ thiếu ý / phải nhìn · ❌ không làm được → ghi một dòng vào
   [review-schedule.md](../notes/review-schedule.md) bảng *Đang tới hạn* (❌ +2 ngày · ⚠️ +5 · ✅ +14).

> Đọc câu hỏi rồi mở đáp án ngay = **vô ích** — cảm giác "à mình biết" là ảo giác quen thuộc.
> Nhớ sai rồi được sửa còn đọng hơn đọc đúng 10 lần.

## Đường đi của một câu hỏi qua hệ thống — mỗi trạm là một thẻ

```
văn bản luật ──[01 chunking]──► các chunk ──► 2 kho: BM25 index + Qdrant (vector)
                                                       │
câu hỏi "phạt vượt đèn đỏ" + cây lọc {"and": [...]}    │
        │                                              ▼
        ├──► nhánh BM25  [02 BM25]  khớp MẶT CHỮ ── lọc bằng matches()  ─┐   [03 metadata filter]
        └──► nhánh dense (BGE → Qdrant) khớp NGHĨA ── Qdrant tự lọc ─────┤   [04 port / adapter]
                                                                         ▼
                                                    [05 RRF] trộn 2 danh sách theo THỨ HẠNG
                                                                         ▼
                                                    top-k điều luật trả về
                                                                         ▼
                              chấm bằng đáp án Zalo: [06 Hit@k] · [07 MRR] · [08 NDCG@k]
```

## Danh sách thẻ — ôn theo thứ tự hạn

| Thẻ | Câu phỏng vấn | Hạn ôn (17/10) |
|---|---|---|
| [01 Recursive chunking](01-chunking.md) | 1.4 | **21/10** |
| [02 BM25](02-bm25.md) | 3.8 | **21/10** |
| [03 Metadata filter + tenant](03-metadata-filter.md) | 3.9 · "vì sao chuyền cây xuống cả hai nhánh" | **20/10** · **21/10** |
| [04 Port / adapter](04-port-adapter.md) | 10.10 · 10.11 | **21/10** |
| [05 Hybrid + RRF](05-hybrid-rrf.md) | 3.5 | **20/10** |
| [06 Hit@k](06-hit-at-k.md) (+ kiểm đầu vào) | 12.1 | — |
| [07 MRR](07-mrr.md) | 12.1 | — |
| [08 NDCG@k](08-ndcg.md) | 12.1 | ôn Cặp 29 sáng 18/10 |

Hạn thật luôn lấy theo [review-schedule.md](../notes/review-schedule.md) — bảng trên chỉ là ảnh chụp ngày 17/10.

## Khi học xong một kỹ thuật mới

Claude tạo thẻ mới **cùng khuôn** (6 mục bên dưới), số lấy từ chạy code thật, rồi thêm 1 dòng vào bảng trên.

```
1. Bài toán        — 2-3 câu: không có nó thì hỏng gì
2. Kiến thức       — đầu vào · thao tác · đầu ra · công thức
3. Ví dụ tính tay  — MỘT bộ số xuyên suốt
4. Code trong repo — đoạn code thật + đọc từng bước
5. Hay lẫn         — bảng đúng ↔ sai (trỏ Cặp trong the-phan-biet)
6. Tự kiểm         — bài tính · câu phỏng vấn · việc tay; đáp án giấu trong ▶
```
