# 🐛 Bug Log — nhật ký bug (cố ý + thật)

> Trái tim của phương pháp học. Mỗi bug (dù **cố ý gài** ở bước 2, hay **gặp thật** khi chạy)
> ghi lại đây. Đọc lại file này = ôn đúng những chỗ mắt người hay trượt.
>
> **Vì sao đáng ghi:** senior không giỏi vì không tạo bug — giỏi vì **nhận ra pattern bug**.
> Ghi 20 bug → lần 21 nhìn phát ra ngay.

**Template:**
```
### #<n> — <tiêu đề ngắn>  ·  Phase <n>  ·  <cố ý | thật>  ·  <ngày>
- **Triệu chứng:** kết quả sai thế nào (số thật: mong đợi X, nhận Y)
- **Nguyên nhân:** dòng nào, sai vì sao
- **Cách tìm ra:** in gì / trace gì để lần ra (đây là phần quý nhất)
- **Fix:** sửa gì
- **Test chặn tái phát:** tên test regression đã thêm
- **Bài học / pattern:** loại bug này còn xuất hiện ở đâu nữa
```

---

## Phân loại pattern hay gặp (điền dần)

| Pattern | Ví dụ kinh điển | Đã dính ở bug # |
|---|---|---|
| Off-by-one | rank bắt đầu từ 0 thay vì 1 (NDCG, RRF) | — |
| Sai dấu / ngưỡng | `>= 0` lẽ ra `>= 0.5`; đảo dấu λ trong MMR | — |
| Quên normalize | cosine trên vector chưa L2-norm | — |
| Thiếu `await` | async lây cả chuỗi, coroutine không chạy | — |
| Parse lỏng | `"yes" in text` bắt nhầm "no ... yes-like" | — |
| Silent failure | quên filter `tenant_id` → rò data, KHÔNG crash | — |
| State/loop guard | thiếu `max_steps`/`attempts` → lặp vô hạn | — |

---

## (Ghi các bug bên dưới, mới nhất trên cùng)
