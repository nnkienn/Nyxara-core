# 📓 Notes — sổ tay học Nyxara

> Bốn cuốn sổ đi kèm [LEARNING_ROADMAP.md](../LEARNING_ROADMAP.md). Roadmap = *bản đồ*
> (làm gì, theo thứ tự nào). Notes = *thứ đọng lại* sau mỗi bước code tay.
> Bước 6 của vòng học ("DOCUMENT") ghi vào đây — **mỗi bước, không để sau.**

| Sổ | Ghi cái gì | Khi nào viết |
|---|---|---|
| [design-system.md](./design-system.md) | Quyết định kiến trúc: hexagonal, port/adapter, Core↔Cloud, quy ước đặt tên/thư mục | Khi thêm 1 tầng/port/adapter mới, hoặc chốt 1 quy ước |
| [algorithms.md](./algorithms.md) | Thuật toán + toán + CTDLGT: công thức, WHY, độ phức tạp | Khi học 1 kỹ thuật (cosine, BM25, RRF, MMR…) |
| [glossary.md](./glossary.md) | Từ mới, 1 dòng/từ | Gặp thuật ngữ lạ bất kỳ |
| [bug-log.md](./bug-log.md) | Nhật ký bug (cố ý + thật): triệu chứng → nguyên nhân → fix → test | Mỗi lần bước 2–5 của vòng học (bug cố ý / debug) |

**Quy tắc vàng:** viết bằng **số thật** và **ví dụ chạy được**, không viết chung chung.
"RRF gộp ranking" ❌ → "RRF: doc A rank 1 ở dense, rank 3 ở BM25 → 1/61 + 1/63 = 0.0323" ✅.
