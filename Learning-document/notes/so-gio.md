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

## Cam kết từ 2026-09-11 (re-plan 10/09 — [LEARNING_ROADMAP.md § RE-PLAN 2026-09-10](../LEARNING_ROADMAP.md))

| Ngày | Sàn | Cố định trong đó | Giờ-mốc |
|---|---|---|---|
| Thứ Hai → Thứ Sáu | **3h** | 10' drill nền + 20' ôn | **2h30** |
| Thứ Bảy, Chủ Nhật | **6h** | 10' + 20' + ~45' trả nợ | **4h45** |

- Trung bình tuần **3.86h/ngày** — nằm trong biên "3-4h/ngày" của cam kết 28/08 **nếu tính trung bình**.
  Nhưng **từng ngày cuối tuần 6h là mức MỚI**, cao hơn trần 4h cũ → ✅ **user chốt 10/09**.
- **Từ 11/09 ghi `giờ-mốc: Xh` ở đầu cột Ghi chú** = giờ thật sự đổ vào mốc (không tính ôn, drill, dọn môi
  trường, sửa note). Đây là số dùng để kiểm giả định ~6h/mốc tại checkpoint 17/09.
- **Hụt 6h một ngày cuối tuần ≈ mất ~1 mốc tháng 9.** Luật lãi 1.5x cho `TRÔI` và trần 6h giữ nguyên.
- Toán cả năm: nhịp thật 03→10/09 là **2h27/ngày** → xong nội dung ~03/03/2027, **sau Tết**. Mức cam kết
  trên là mức **tối thiểu** để xong ~30/12/2026.

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
| 2026-09-09 | Tư | 3h00 | 2h00 (sáng 6:00-7:30 · tối 30') | −1h00 | BKK | **4h15** | Ca sáng: drill ép chọn 9/13 · Cặp 12 vá bằng bài đo. **Ca tối chỉ 30': bài trace `merge_pieces` mèo/chó — user tự báo "hoàn toàn mù", 0 dòng code, Claude sửa ~3 lần bằng lời không ăn.** Xếp `BKK` chứ không `TRÔI`: có ngồi làm thật, tắc vì bài giao sai cách (xem [review-schedule.md § 10/09](./review-schedule.md)) |
| 2026-09-10 | Năm *(ca chiều)* | 3h00 | ~2h00 (15:12-~17:15) | — | — | *(gộp sau ca tối)* | Làm bù tối 09/09. Trace tay `merge_pieces` input mới: cột `current_merge` đúng 6/6 vòng, cột `merges` sai 3 ô → lòi **6 lỗ nền Python, không lỗ nào là chunking**. Mốc tự kiểm 10/09 → chọn **ngày B** (vá nền đọc code) |
| 2026-09-10 | Năm *(ca tối, máy Mac)* | — | ~1h11 (21:47-22:58, gồm ~18' báo cáo + re-plan) | — | BKK | **~4h04** | Ngập. Cả ngày ~3h11 vs sàn 3h → +11'. Áp §3.9: drill đọc-chạy **8/9** · tự tìm ra input **ca túi cuối** · drill list↔set↔dict **3/6** chưa sạch · **báo cáo mốc tự kiểm + RE-PLAN tháng 9** (user chốt: 6h T7/CN + phương án B). *(RE-PLAN tính với nợ 4h25 — để nguyên, dư an toàn)* |
| 2026-09-11 | Sáu *(ca sáng)* | 3h00 | 45' (07:06-07:51) | — | — | *(gộp sau ca tối)* | giờ-mốc: ~30'. Drill list↔set↔dict 4/6 + ép chọn 3/6 (đảo dấu `:`), chưa sạch · tự viết lại `merge_pieces` đóng sách 4/5 ca; sửa bug chunk rỗng 5 lượt chưa xong (lần cuối thụt lề sai → mất mẩu) · VS Code không lưu được xuống đĩa từ 07:25. **Tối phải thêm 2h15** để đạt sàn 3h |
| 2026-09-11 | Sáu *(ở công ty)* | — | ~2h25 đo được (10:07-11:50 · 16:40-17:25) **+ giờ ngồi quán (chưa ghi)** | — | — | **≤ ~3h49** *(chưa trừ giờ quán + ca tối)* | giờ-mốc: **0**. Công ty rảnh. Drill list↔set↔dict 4/6 → 0/2 → 2/3 (còn lỗ set bỏ trùng khi `.add`) · +7 CRAG không nhớ → dựng lại bằng trace thật → code tay schema xanh lượt 4 · `make_grade_node` còn nợ · lòi [bug #33](./bug-log.md). Cả ngày tới 17:25 = 45' + ~2h25 = **~3h10 ≥ sàn 3h** kể cả chưa tính giờ quán. ⚠️ Đạt sàn giờ nhưng **giờ-mốc cả ngày chỉ ~30'** — ôn phình ra chiếm gần hết |
| 2026-09-11 | Sáu *(ca tối, máy Mac)* | — | ~40' (23:31-00:10) | — | — | **≤ ~3h14** *(chưa trừ giờ quán)* | giờ-mốc: **0**. Cả ngày ~45' + ~2h25 + ~40' ≈ **3h50 + giờ quán** → đạt sàn. Tối: tìm ra gốc lỗi VS Code (mở thư mục cha làm gốc → settings bị bỏ qua) · sửa máy chấm CRAG cho Python 3.9 · **2a `make_grade_node` ✅** (khung điền chỗ trống). T7 12/09 đi làm (một lần) |

> **Tình trạng 10/09 (cuối ngày, 22:58):** nợ **~4h04**, vẫn toàn `BKK` (ngập). Cách trần 6h còn **~1h56**
> → **11/09 hụt quá 1h35 là chạm trần**, mất trọn 1 buổi re-plan. Ca sáng 11/09 là ca phải giữ bằng mọi giá.
>
> *(cũ)* **Tình trạng 10/09 (sau ca chiều):** nợ **4h15**, vẫn toàn `BKK`. Ca tối cam kết 3h → ngày 10/09 tổng
> ~5h vs sàn 3h → trả 2h → nợ còn **2h15**. ⚠️ Nếu ca tối **không** diễn ra: ngày 10/09 thiếu 1h → nợ
> **5h15, sát trần 6h** — thêm một ngày hụt nữa là chạm trần, cấm học kỹ thuật mới 1 buổi.
>
> 🌧️ **Cập nhật 21:47 (máy Mac):** ca tối **không được 3h** — ngập, chỉ ~1h05. Ngày 10/09 ≈ 2h +
> 1h05 = **3h05** vs sàn 3h → dư 5' → nợ còn ≈ **4h10** (không phải 2h15). Vẫn `BKK`, chưa chạm
> trần 6h, nhưng còn cách trần **chưa tới 2h**.
>
> *(cũ, cuối ngày 09/09 — ghi trên máy Mac)* 🔍 **Phát hiện đáng giá nhất của ngày, ảnh hưởng thẳng tới cách xếp lịch:** **lỗi của user hôm
> nay gần như 100% là lỗi CHÚ Ý, không phải lỗi hiểu.** Đếm được: `len("Meo")=2` (đọc chỉ số cuối
> thay vì độ dài) · kéo ô `0` của lượt 1 xuống lượt 2 · nhét `current_merge` vào `merges` ở nhánh
> `if` (2 lần) · nhìn nhầm `if` dòng 35 thành `if` dòng 29 · chọn `attempts` vì nó đang mở trên màn
> hình · gắn `fixed_size_chunk` vào retriever. **Và chúng tăng dần theo độ mệt:** ca sáng 9/13 với
> mấy câu trả lời rất chắc, ca tối lệch một ô mỗi dòng bảng.
> → **Hệ quả xếp lịch: ca sáng đáng giá hơn ca tối rất nhiều đối với user này.** Ca tối sau OT có
> thể cho sản lượng gần bằng 0 mà vẫn tốn giờ. Cân nhắc: buổi nào OT về sau 21h thì **đổi nội dung
> ca tối sang loại ít cần chú ý** (drill ép chọn, giảng lại bằng lời) thay vì trace/đọc code, và
> dồn việc đọc code sang sáng.
>
> ⚠️ **Sửa lại ngày 10/09 — câu "gần như 100% là lỗi CHÚ Ý" ở trên NÓI QUÁ.** Ca chiều 10/09, lúc
> **tỉnh táo** (15:12), user vẫn sai cột `merges` 3 ô, và bóc ra 6 lỗ nền *mô hình chạy Python*
> (thụt lề = phạm vi · luồng `for` · `+=` chuỗi ↔ `append` list · giá trị biến tại đúng lúc dòng chạy ·
> `{}` set ↔ `[]` list). Tức là: **mệt KHUẾCH ĐẠI lỗi, nhưng gốc là lỗ hổng HIỂU thật.** Luật xếp
> việc theo giờ (CLAUDE.md §3.9) vẫn giữ — chỉ sửa lý do: ngủ đủ **không tự vá** được lỗ nền, phải
> drill đọc-chạy (ngày B).
>
> *(cũ)* **Tình trạng 09/09 (đầu buổi):** nợ **3h15**, vẫn toàn bộ `BKK`, chưa phát sinh lãi, chưa chạm
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
