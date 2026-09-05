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
| 2026-09-06 | CN | 3h00 | *(kế hoạch 6h)* | *+3h* | — | *dự kiến **0*** | Trạm 4 (3h) + fix bug #25 (3h). Đủ 6h là trả sạch nợ và đóng sổ Phase 0 |

> **Tình trạng 05/09:** nợ **1h30**, toàn bộ vẫn là `BKK` (3 ngày liên tiếp OT/mệt, không có
> ngày nào `TRÔI` → chưa phát sinh lãi, chưa chạm trần 6h). CN 06/09 làm đủ 6h là về 0.
>
> *(cũ 04/09)* nợ 2h00, **toàn bộ là `BKK`** (03/09 mệt sau 2 ca, 04/09 OT) → chưa phát
> sinh lãi, chưa chạm trần 6h. Nhưng nợ vẫn là nợ: buổi T7 05/09 là buổi trả nợ, không phải buổi
> dư dả.
