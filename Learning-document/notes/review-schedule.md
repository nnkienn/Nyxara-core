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
| Incremental ingest / multi-store diff (`manifest` = `{tenant:{doc:{idx:hash}}}`, `diff_manifest`, `to_upsert/skip/delete`) | 2026-09-02 | ⬜ 2026-09-03 | ⬜ 2026-09-05 | ⬜ 2026-09-09 | ⬜ 2026-09-16 | qua cổng đóng-sách Trạm 1 hôm nay (retrace Method 2.0) |
| Retrieval 2 tầng (rẻ-rộng Dense+BM25+RRF → đắt-hẹp cross-encoder) + hợp đồng return giữa 2 retriever | 2026-09-02 | ⬜ 2026-09-03 | ⬜ 2026-09-05 | ⬜ 2026-09-09 | ⬜ 2026-09-16 | qua cổng Trạm 2. **Ôn kỹ 2 chỗ từng lẫn:** (1) cross-encoder ĐẮT+HẸP, không pre-compute được — không phải "rẻ và rộng"; (2) cross-encoder ≠ RRF, và cross-encoder KHÔNG thuộc CRAG |

> Thêm hàng mới mỗi khi 1 kỹ thuật qua checkpoint (e) trong roadmap. Đừng xoá hàng cũ dù đã
> ôn hết 4 mốc — giữ lại làm log, chỉ ngừng thêm cột ôn tiếp.
