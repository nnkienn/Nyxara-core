# 🔁 Lịch ôn cách quãng (spaced repetition)

> Nguồn gốc: [LEARNING_ROADMAP.md § Phương pháp học 2.0](../LEARNING_ROADMAP.md) (thêm
> 2026-08-28, sau khi nhận ra 6.5 tuần đầu đọng lại yếu). Cách dùng ở đầu mỗi buổi:
> 1. Xem hàng nào có ngày ôn (+1/+3/+7/+14) ≤ hôm nay và chưa tick.
> 2. Làm **(b) giảng lại** (đóng tài liệu, nói/viết lại nguyên lý) cho mọi hàng tới hạn.
> 3. Với hàng ở cột +7 hoặc +14: thêm **(c) code-tay-lại** phần lõi thuật toán (10-15 phút,
>    không nhìn file cũ), rồi so với code thật.
> 4. Tick ✅ vào đúng cột ngày đã ôn xong. Nếu giảng lại/code lại không trôi chảy → đừng tick,
>    quay lại đọc note gốc củng cố trước, ôn lại hôm sau.

| Kỹ thuật | Xong ngày | +1 | +3 | +7 | +14 | Ghi chú |
|---|---|---|---|---|---|---|
| BM25 scoring (IDF, k1, b) | 2026-08-03 | — | — | — | — | *(đã qua ngày, ôn khi tới lượt active-recall)* |
| RRF (Reciprocal Rank Fusion) | 2026-08-03 | — | — | — | — | |
| Cross-encoder rerank (bi- vs cross-encoder) | 2026-08-04 | — | — | — | — | |
| CRAG state machine (`decide()`, `attempts` guard) | 2026-08-12 | — | — | — | — | |
| Incremental ingest / multi-store diff (`manifest` = `{tenant:{doc:{idx:hash}}}`, `diff_manifest`, `to_upsert/skip/delete`) | 2026-09-02 | ⚠️ 2026-09-03 **TRƯỢT rồi vá** | ⬜ 2026-09-04 *(ôn bù)* | ⬜ 2026-09-09 | ⬜ 2026-09-16 | Qua cổng Trạm 1 ngày 02/09 nhưng +1 hôm sau trượt. Lẫn `to_upsert`/`to_delete` **lần thứ 4** và đảo ngược bền/dễ vỡ. Đã vá bằng drill ([the-phan-biet.md](./the-phan-biet.md) Cặp 1, 2, 8) → 11/12. **Chưa tick sạch — phải ôn bù 04/09 rồi mới tính +3.** |
| Retrieval 2 tầng (rẻ-rộng Dense+BM25+RRF → đắt-hẹp cross-encoder) + hợp đồng return giữa 2 retriever | 2026-09-02 | ⚠️ 2026-09-03 **TRƯỢT rồi vá** | ⬜ 2026-09-04 *(ôn bù)* | ⬜ 2026-09-09 | ⬜ 2026-09-16 | +1 trượt: tưởng BM25 là model / cross-encoder không phải, và cross-encoder "đắt và **rộng**". Đã vá bằng drill (Cặp 3, 4, 5, 6) → 11/12. **Chưa tick sạch — ôn bù 04/09.** |

> Thêm hàng mới mỗi khi 1 kỹ thuật qua checkpoint (e) trong roadmap. Đừng xoá hàng cũ dù đã
> ôn hết 4 mốc — giữ lại làm log, chỉ ngừng thêm cột ôn tiếp.

---

## 🃏 Luật bổ sung (thêm 2026-09-03, sau khi mốc +1 đầu tiên trượt)

Mốc +1 đầu tiên áp dụng thật đã **trượt 3/4 câu** dù hôm trước đã qua cổng đóng-sách. Rút ra:

1. **Qua cổng đóng-sách KHÔNG có nghĩa là đã đọng lại.** Cổng chỉ chứng minh "hiểu được ngay sau
   khi vừa được sửa". Mốc +1 hôm sau mới là phép thử thật. Đừng coi cổng là xong.
2. **Phân loại lỗi trước khi chữa.** Lỗi *quên* (không nhớ ra) ≠ lỗi *phân biệt* (lẫn 2 thứ na ná
   nhau). Nếu các câu sai đều có dạng "chọn nhầm giữa A và B" → **đừng giải thích lại**, giải
   thích lại không ăn (đã thử, 12 tiếng sau vẫn lẫn). Chuyển sang **drill phân biệt**:
   ~12 câu ép chọn A/B, trả lời liên tục, sửa 1 lượt cuối. Nội dung lấy từ
   [the-phan-biet.md](./the-phan-biet.md). Hiệu quả thật: 1/4 → 11/12 trong 1 vòng.
   Cùng cơ chế với drill cú pháp Python (§3.5 CLAUDE.md) — chỉ khác nội dung.
3. **Trượt +1 thì không tick, và chèn 1 buổi "ôn bù" ngày hôm sau** trước khi tính tiếp mốc +3.
   Ghi rõ trượt ở cặp/khái niệm nào vào cột Ghi chú — để lần sau nhắm thẳng vào đó.
4. **Không mở trạm/kỹ thuật mới trong buổi mà mốc ôn bị trượt.** Ưu tiên vá nền trước
   (đúng §3.6 mục 5 — checkpoint đóng-sách). Đã áp dụng thật sáng 03/09: hoãn Trạm 3 sang ca tối.
