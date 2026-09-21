# 📓 Notes — sổ tay học Nyxara

> Đi kèm [LEARNING_ROADMAP.md](../LEARNING_ROADMAP.md) (*bản đồ*: làm gì, theo thứ tự nào) và
> [phases.md](../phases.md) (*kho kiến thức* 10 Phase, tra cứu). Notes = *thứ đọng lại* sau mỗi bước code tay. Bước 6 của vòng học ("DOCUMENT") ghi vào
> đây — **mỗi bước, không để sau.**

| Sổ | Ghi cái gì | Khi nào viết |
|---|---|---|
| [design-system.md](./design-system.md) | Quyết định kiến trúc: hexagonal, port/adapter, Core↔Cloud, quy ước đặt tên/thư mục | Khi thêm 1 tầng/port/adapter mới, hoặc chốt 1 quy ước |
| [algorithms.md](./algorithms.md) | Thuật toán + toán + CTDLGT: công thức, WHY, độ phức tạp | Khi học 1 kỹ thuật (cosine, BM25, RRF, MMR…) |
| [glossary.md](./glossary.md) | Từ mới, 1 dòng/từ | Gặp thuật ngữ lạ bất kỳ |
| [bug-log.md](./bug-log.md) | Nhật ký bug (cố ý + thật): triệu chứng → nguyên nhân → fix → test | Mỗi lần bước 2–5 của vòng học (bug cố ý / debug) |
| [the-phan-biet.md](./the-phan-biet.md) | **Cặp dễ lẫn** + nhật ký drill ép chọn | Mỗi khi lẫn 2 thứ na ná nhau — drill ép chọn, **không** giảng lại (1/4 → 11/12 trong một vòng) |
| [review-schedule.md](./review-schedule.md) | Lịch ôn đang tới hạn + nhật ký buổi (**tối đa ~15 dòng/buổi**) + chỗ dừng | Đầu buổi đọc, cuối buổi ghi |
| [english-speaking.md](./english-speaking.md) | Bản tiếng Anh **user tự viết** + bản Claude chỉnh (giữ nguyên ý) + bảng lỗi lặp lại | Mỗi slot tiếng Anh ở ca công ty — viết trước, chỉnh sau, **đọc TO** rồi tick |
| [pipeline/](./pipeline/README.md) | Sơ đồ trace luồng document→CRAG→answer, **theo đúng thứ tự chạy thật** (4 file: ingest → retrieval → crag → api), kèm bẫy/bug thật gặp ở từng chặng | Sau khi ráp xong 1 chặng lớn (không phải 1 hàm nhỏ) — vd xong cả pipeline ingest, xong cả `/ask` |

**Quy tắc vàng:** viết bằng **số thật** và **ví dụ chạy được**, không viết chung chung.
"RRF gộp ranking" ❌ → "RRF: doc A rank 1 ở dense, rank 3 ở BM25 → 1/61 + 1/63 = 0.0323" ✅.
