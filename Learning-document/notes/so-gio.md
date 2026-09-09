# ⏱️ Sổ nợ giờ

> Lập 2026-09-04 theo yêu cầu của user ("nếu không đạt cam kết thì đề xuất phương án phạt").
> Gắn với [LEARNING_ROADMAP.md § DEADLINE ÉP TIẾN ĐỘ](../LEARNING_ROADMAP.md): cam kết **sàn 3h/ngày**
> (biên độ 3-4h). Toàn bộ bài toán deadline 31/12/2026 chỉ đóng được ở mức này — ~437h khả dụng
> so với ~400-420h cần, gần như không có slack. Nên nợ giờ = deadline lùi thật, không phải cảm giác.

## Luật

1. **Ghi mỗi buổi 3 số:** cam kết / thực tế / nợ lũy kế. Ghi cả ngày nghỉ (thực tế = 0).
2. **Phân loại nợ:**
   - `BKK` — bất khả kháng (OT, ốm, việc gia đình). **Vẫn phải trả**, nhưng **không bị phạt lãi**.
   - `TRÔI` — rảnh mà không học, hoặc mở máy ra rồi trôi. **Bị lãi 1.5x**.
3. **Lãi 1.5x:** mỗi 1h nợ loại `TRÔI` phải trả bằng **1h30**, hạn **7 ngày**, cắt vào thời gian
   giải trí. Lý do chọn phạt bằng giờ chứ không bằng tiền: tiền không mua lại được giờ, mà thứ
   đang thiếu là giờ.
4. **Trần nợ 6h:** nợ lũy kế vượt 6h → **cấm học kỹ thuật mới 1 buổi**, dành trọn buổi đó ngồi
   re-plan lại roadmap bằng số thật. Đây là phạt tự nhiên: phải tự nhìn deadline lùi.
5. **Không bao giờ dùng làm phạt:** cắt giấc ngủ · bỏ bước trong vòng 6 bước · bỏ buổi ôn cách
   quãng. Ba thứ đó phá đúng cái đang xây, phạt kiểu đó là tự bắn vào chân.

## Nhật ký

| Ngày | Thứ | Cam kết | Thực tế | Chênh | Loại | Nợ lũy kế | Ghi chú |
|---|---|---|---|---|---|---|---|
| 2026-09-03 | Năm | 3h00 | 2h15 | −45' | BKK | **45'** | 2 ca: sáng 6h15-7h15 (ôn +1 trượt → drill phân biệt) · tối ~1h (mở Trạm 3, dừng vì mệt) |
| 2026-09-04 | Sáu | 3h00 | 1h45 | −1h15 | BKK | **2h00** | OT về trễ, 21:42-23:30. Ôn bù 9.5/10 · drill Cặp 9 vòng 2 · Trạm 3 xong phần hiểu |
| 2026-09-05 | Bảy | 3h00 | ~3h30 (19:55-00:05, nghỉ 2×20') | +30' | BKK | **1h30** | OT chiều nên mất ca 14:00-16:30 của kế hoạch. Ca tối: drill closure 4/4 · **tự code xong fix bug #26** · tự viết 2 test bắt quá trình · phát hiện + fix bug #27 → suite **68 xanh** (lần đầu xanh sau 8 ngày) · làm luôn Trạm 4a phần chẩn đoán |
| 2026-09-06 | CN | 3h00 | ~4h00 (13:30-17:30) | +1h00 | — | **30'** | Đổi máy → mất ~40' dựng lại `.venv` + tải 4.4GB weights. Trạm 4b ✅ · Trạm 4c ✅ · **fix thật bug #25** (treo 23 ngày) · phát hiện + fix **bug #31** (lifespan không dọn model → CUDA OOM) · suite **70 passed**. Dừng sớm vì đổi máy, chưa làm 4d / bug #29 / `split_by_separators` |
| 2026-09-06 | CN *(ca tối)* | — | 1h15 (20:45-22:00) | — | — | **0** *(dư 45')* | Cùng ngày tính gộp **5h15 vs sàn 3h → trả sạch nợ, dư 45'**. Trạm **4d** ✅ (hết bài trace 4 trạm) · **fix bug #29** + test race, tự chứng minh test đỏ được (7560/8000) · đổi tên `fixed_size_chunk`, vấp [bug #32](./bug-log.md) → **71 passed** |
| 2026-09-07 | Hai | 3h00 | ~2h00 (20:45-22:41) | −1h00 | BKK | **15'** | Ôn trượt nặng phải vá tại chỗ → lòi lỗ hổng cú pháp Python, phải chèn drill 6 bài (6/6). Cặp 10 `def`↔`async def` vá bằng **tự đo** 2.05s/6.02s sau khi sai 4 lượt. `diff_manifest` 4/4 → Cặp 1 sạch. **`merge_pieces` — hàm đầu tiên user tự viết trọn vẹn, không Copilot.** Dừng vì mệt. Suite 71 passed |
| 2026-09-08 | Ba | 3h00 | **0h** | −3h00 | BKK | **3h15** | **NGHỈ — OT.** Không mở máy. Commit `0ecef0e` lúc 18:53 chỉ là commit lại phần việc của buổi 07/09, không phải giờ học mới |
| 2026-09-09 | Tư | 3h00 | ~2h10 (6:00-7:30 · 21:30-22:01) | −50' | BKK | **4h05** | Sáng: drill 13 câu 9/13 · **Cặp 12 mới** vá bằng bài đo · code-tay CRAG trả 1/3. Tối OT về 21:30, dừng 22:01 — user tự báo *"không đủ tỉnh táo đọc code"*, chấp nhận trễ hẹn chunker 1 ngày. Trace `merge_pieces` mới xong 4/7 dòng |

> **Tình trạng 09/09 (cuối ngày):** nợ **4h05**, vẫn toàn bộ `BKK` (OT 3 buổi trong 6 ngày),
> chưa phát sinh lãi. **Nhưng đã đi 2/3 đường tới trần 6h** — chạm trần là mất trọn 1 buổi để
> re-plan, tức mất thêm 3h nữa. Hai ngày tới mà còn OT thì chạm.
>
> 🔍 **Phát hiện đáng giá nhất của ngày, ảnh hưởng thẳng tới cách xếp lịch:** **lỗi của user hôm
> nay gần như 100% là lỗi CHÚ Ý, không phải lỗi hiểu.** Đếm được: `len("Meo")=2` (đọc chỉ số cuối
> thay vì độ dài) · kéo ô `0` của lượt 1 xuống lượt 2 · nhét `current_merge` vào `merges` ở nhánh
> `if` (2 lần) · nhìn nhầm `if` dòng 35 thành `if` dòng 29 · chọn `attempts` vì nó đang mở trên màn
> hình · gắn `fixed_size_chunk` vào retriever. **Và chúng tăng dần theo độ mệt:** ca sáng 9/13 với
> mấy câu trả lời rất chắc, ca tối lệch một ô mỗi dòng bảng.
> → **Hệ quả xếp lịch: ca sáng đáng giá hơn ca tối rất nhiều đối với user này.** Ca tối sau OT có
> thể cho sản lượng gần bằng 0 mà vẫn tốn giờ. Cân nhắc: buổi nào OT về sau 21h thì **đổi nội dung
> ca tối sang loại ít cần chú ý** (drill ép chọn, giảng lại bằng lời) thay vì trace/đọc code, và
> dồn việc đọc code sang sáng.

> *(cũ, đầu buổi 09/09)* **Tình trạng 09/09 (đầu buổi):** nợ **3h15**, vẫn toàn bộ `BKK`, chưa phát sinh lãi, chưa chạm
> trần 6h. Hôm nay cam kết 4h30 (1h30 sáng + 3h tối) vs sàn 3h → trả 1h30, cuối ngày còn **1h45**.
> ⚠️ **Rủi ro thật không phải con số nợ** mà là: **recursive chunker sang ngày thứ 3 vẫn chưa đóng**
> (07/09 xong 1 hàm · 08/09 nghỉ · 09/09 sáng ăn hết vào ôn). Luật "1 kỹ thuật / 2 ngày" đã trượt.
> Mốc tự kiểm **10/09** phải re-plan thật, đừng để trôi.
>
> *(cũ 07/09)* **Tình trạng 07/09:** nợ **15'** (dư 45' từ 06/09 − 1h thiếu hôm nay), vẫn toàn bộ `BKK`,
> chưa chạm trần 6h, chưa phát sinh lãi. Buổi ngắn (2h) nhưng **không phải buổi trôi**: 4 hạng mục
> vá nền + 1 hàm tự viết. Rủi ro thật không nằm ở 1h thiếu này mà ở chỗ **chunker chưa xong** —
> nếu 08/09 vẫn chưa khép được thì luật "1 kỹ thuật / 2 ngày" bắt đầu trượt, và mốc tự kiểm 10/09
> sẽ phải re-plan thật.
>
> *(cũ 06/09)* nợ còn **30'**, vẫn toàn bộ `BKK`. Kế hoạch 6h không đạt (làm ~4h, dừng
> vì đổi máy) nhưng vẫn dư 1h so với sàn 3h → trả được 1h nợ. Chưa chạm trần 6h, chưa phát sinh lãi.
> **Việc trôi sang buổi sau:** Trạm 4d · fix bug #29 · nối `split_by_separators` — tức là
> **Phase 0 chưa đóng sổ** như kế hoạch. Cần tính lại lịch tháng 9 nếu buổi 07/09 vẫn phải vá nền.
>
> *(cũ 05/09)* nợ **1h30**, toàn bộ vẫn là `BKK` (3 ngày liên tiếp OT/mệt, không có
> ngày nào `TRÔI` → chưa phát sinh lãi, chưa chạm trần 6h). CN 06/09 làm đủ 6h là về 0.
>
> *(cũ 04/09)* nợ 2h00, **toàn bộ là `BKK`** (03/09 mệt sau 2 ca, 04/09 OT) → chưa phát
> sinh lãi, chưa chạm trần 6h. Nhưng nợ vẫn là nợ: buổi T7 05/09 là buổi trả nợ, không phải buổi
> dư dả.
