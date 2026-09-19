# SÁNG 20/09 — BÀI GHÉP DÒNG (Parsons) · `to_qdrant_filter`

> Làm bài này **sau** khi đã ĐOÁN → CHẠY → SOI file
> [2026-09-20-primm-to-qdrant-filter.py](./2026-09-20-primm-to-qdrant-filter.py), và **đóng file đó lại**.
>
> Vì sao ghép dòng thay vì gõ từ trắng: người mới đốt gần hết trí nhớ làm việc vào **nhớ cú pháp**
> và **giải mã lỗi** — đúng cái đã giết buổi 19/09 (`nam`/`năm`, `C` hoa, thiếu `}`). Bỏ gánh đó đi
> thì đầu còn chỗ để nghĩ về **logic**. Học được ngang gõ từ trắng, nhanh hơn, không tắc cứng.

---

## Bài 1 — nhánh `and`

Các dòng dưới đây **đúng hết**, chỉ bị **xáo thứ tự**, và **hai dòng thừa** không thuộc về bài (bẫy).
Chép ra, sắp lại cho đúng thứ tự + đúng mức thụt lề.

```
A)     return {"must": danh_sach_con}
B)     danh_sach_con.append(to_qdrant_filter(con))
C)     for con in pred["and"]:
D)     danh_sach_con = []
E)     if phep == "and":
F)     return danh_sach_con                      <- thừa?
G)     danh_sach_con.append(con)                 <- thừa?
```

Viết đáp án dạng: `E → ... → ...`, và nói **một câu** vì sao hai dòng kia là bẫy.

## Bài 2 — nhánh so số (`gt/gte/lt/lte`)

```
A)     return {"key": ten_truong, "range": {phep: gia_tri}}
B)     gia_tri = pred[phep][1]
C)     if phep in SO_SANH_SO:
D)     ten_truong = pred[phep][0]
E)     return {"key": ten_truong, "range": {"gte": gia_tri}}     <- thừa?
```

Đáp án + **một câu**: dòng E sai ở đâu, và nó sẽ sai **âm thầm** hay **nổ ra lỗi**?

## Bài 3 — nhánh `not`

```
A)     return {"must_not": [to_qdrant_filter(pred["not"][0])]}
B)     if phep == "not":
C)     return {"must_not": to_qdrant_filter(pred["not"][0])}      <- thừa?
D)     return {"must_not": [to_qdrant_filter(pred["not"])]}       <- thừa?
```

Đáp án + **một câu cho mỗi dòng thừa**: nó khác dòng đúng ở đúng ký tự nào.

---

## Sau cùng — GÕ LẠI TỪ TRẮNG

Đóng hết. Mở file trắng, gõ lại cả hàm `to_qdrant_filter`, tên biến **tiếng Anh**
(`operator` · `field` · `value` · `children`). Chạy lại bộ ca thử của file PRIMM để tự chấm.

**Đây mới là chỗ tính điểm.** Ghép dòng đúng hết mà gõ lại không nổi = chưa thuộc, làm lại vòng nữa.
