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
| Incremental ingest / multi-store diff (`manifest` = `{tenant:{doc:{idx:hash}}}`, `diff_manifest`, `to_upsert/skip/delete`) | 2026-09-02 | ⚠️ 2026-09-03 **TRƯỢT rồi vá** | ✅ 2026-09-04 *(ôn bù: 9.5/10)* | ⬜ 2026-09-09 | ⬜ 2026-09-16 | Qua cổng Trạm 1 ngày 02/09 nhưng +1 hôm sau trượt. Lẫn `to_upsert`/`to_delete` **lần thứ 4** và đảo ngược bền/dễ vỡ. Đã vá bằng drill ([the-phan-biet.md](./the-phan-biet.md) Cặp 1, 2, 8) → 11/12. **Chưa tick sạch — phải ôn bù 04/09 rồi mới tính +3.** |
| Retrieval 2 tầng (rẻ-rộng Dense+BM25+RRF → đắt-hẹp cross-encoder) + hợp đồng return giữa 2 retriever | 2026-09-02 | ⚠️ 2026-09-03 **TRƯỢT rồi vá** | ✅ 2026-09-04 *(ôn bù: 9.5/10)* | ⬜ 2026-09-09 | ⬜ 2026-09-16 | +1 trượt: tưởng BM25 là model / cross-encoder không phải, và cross-encoder "đắt và **rộng**". Đã vá bằng drill (Cặp 3, 4, 5, 6) → 11/12. **Chưa tick sạch — ôn bù 04/09.** |
| CRAG closure vs state (`build_graph` 1 lần lúc boot · `candidate_k` đông cứng · van `max_attempts`) | 2026-09-04 | ✅ 2026-09-05 *(code tay, không chỉ giảng lại)* | ⬜ 2026-09-07 | ⬜ 2026-09-11 | ⬜ 2026-09-18 | Trạm 3 xong phần **hiểu**, chưa qua phần **làm**. Cặp 9 drill 2 vòng vẫn còn sai `max_attempts` + bài closure Python thuần. Mốc +1 (05/09) phải kèm **code tay bản fix #26**, không chỉ giảng lại. |

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

---

## ✅ Buổi 2026-09-04 — đã xong (ôn bù 9.5/10, đã tick +3 cho cả 2 hàng)

## ✅ Buổi 2026-09-05 — đã xong (xem CLAUDE.md §6). Mốc +1 hàng CRAG tick bằng **code tay**, không phải giảng lại suông.

## 📌 Buổi 2026-09-06 (CN, kế hoạch 6h) — ĐÓNG SỔ PHASE 0

> Mục tiêu của buổi này **không phải học thêm**, mà là **dọn sạch tồn đọng** để thứ Hai 07/09 vào
> kỹ thuật mới với sổ sạch. Đừng để nó thành buổi vá nền thứ sáu liên tiếp.

1. **Ca 1 (~3h) — Trạm 4 (API/wiring)**, câu 4a→4d trong
   [pipeline/00-trace-exercises.md](./pipeline/00-trace-exercises.md). Nhẹ hơn Trạm 3 (không có
   closure), và câu 4c hỏi thẳng về bug #25 nên nó dẫn luôn sang ca 2.
2. **Ca 2 (~3h) — fix bug #25 thật** + test chặn tái phát. Đây là "việc làm bằng tay" của Trạm 4
   theo luật mới, đồng thời là milestone riêng trong roadmap tháng 9.
3. Còn giờ → nối `split_by_separators` (~1h, milestone nhỏ nhất còn lại của Phase 0).
4. Mốc ôn **+3** của hàng CRAG rơi vào 07/09 — nhớ code-tay-lại phần lõi, đừng chỉ giảng lại.

> ⚠️ **Luật mới rút ra tối 05/09 (bug #27):** trước khi commit phải chạy `pytest -q` **toàn bộ**,
> không giới hạn thư mục, và đọc `git diff` chứ đừng tin message mình vừa gõ.

## 📌 (lưu trữ) Buổi 2026-09-05 — thứ tự đã chốt tối 04/09

> **Lý do buổi này đổi trọng tâm:** cuối buổi 04/09 user tự báo — *"tôi chỉ hiểu chứ hoàn toàn
> code lại không được, fix bug không được luôn"*. Đây là đúng lỗ hổng mà cả roadmap tồn tại để
> bịt (mục tiêu là **tự implement lõi + tự debug**, không phải đọc-hiểu). Nên T7 **không trace
> thêm trạm mới** — chuyển sang **làm bằng tay**, lấy chính bug #26 làm bài tập vì nó nhỏ, đã
> hiểu rõ, và có sẵn tiêu chí đúng/sai.

**Ca chiều 14:00-16:30 — CODE TAY (không nhìn gợi ý, sai cũng cứ chạy rồi sửa):**
1. Sửa `retrieve_node` để `candidate_k` đọc được từ `state` (closure tụt xuống làm default).
2. Sửa `grade_node` để khi `verdict == "INCORRECT"` thì ghi `candidate_k` lớn hơn vào state.
3. Chạy lại kịch bản grader-luôn-`False`, tự in ra và tự xác nhận dãy `candidate_k` đã tăng dần.
4. Viết **2 test**: (a) dãy `candidate_k` qua từng vòng là tăng dần — *không* phải chỉ assert
   output cuối (test nhìn output cuối sẽ **xanh giả**, đây là bẫy chính); (b) verdict `CORRECT`
   ngay vòng 1 → retriever chỉ được gọi **đúng 1 lần**.

**Ca tối 19:00-21:30:**
5. Mốc ôn +1 của hàng CRAG (giảng lại **và** code lại phần lõi vừa sửa, không nhìn file).
6. Tự kể lại bug #26 + đoạn sửa `03-crag.md` bằng lời mình (2 file đó hiện do Claude viết).
7. Còn thời gian → mở **Trạm 4 (API)** 4a.

> Nếu ca chiều thấy tắc ở **cú pháp Python** chứ không phải logic → dừng, làm drill cú pháp ngắn
> (§3.5 CLAUDE.md), đúng như đã làm hiệu quả 28/08 và 01/09. Đừng ép tiếp.

## 📌 (lưu trữ) Buổi 2026-09-04 — thứ tự đã chốt tối 03/09

1. **Ôn bù 2 hàng đang treo** (Incremental ingest · Retrieval 2 tầng) — chưa được tick, chưa được
   tính mốc +3. Nhắm thẳng vào cặp đã sai: Cặp 1, 2, 8 và Cặp 3, 4, 5, 6 trong
   [the-phan-biet.md](./the-phan-biet.md). Trôi chảy → tick cột +3 ngày 04/09; không trôi → lại
   ôn bù, đừng tick.
2. **Drill Cặp 9 (state ↔ closure)** — cặp mới thêm tối 03/09, sai 4/4 ô, **chưa drill lần nào**.
   ~6 câu ép chọn state/closure, trả lời liên tục, sửa 1 lượt cuối.
3. **Chỉ khi 1 và 2 xong** mới quay lại phần còn nợ của Trạm 3 (bảng trace số thật + teach-back +
   tự sửa note `03-crag.md` + ghi bug-log) — xem
   [pipeline/00-trace-exercises.md § TRẠM 3](./pipeline/00-trace-exercises.md).

> Ca tối 03/09 dừng sớm vì **mệt**, không phải vì nội dung quá khó — user chọn "mệt, muốn dừng"
> khi được hỏi thẳng. Không suy ra là hụt kiến thức nền LangGraph; tầng đó chưa kiểm tra được.
