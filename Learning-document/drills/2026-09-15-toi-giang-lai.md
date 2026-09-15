# Ca 22:00-23:00 ngày 15/09: GIẢNG LẠI ĐÓNG SÁCH

**Luật:** đóng file `toi-mot-luat.py`, đóng chat, đóng note. Gõ câu trả lời ngay dưới mỗi câu, bằng lời của bạn.
Không chạy code. Sai cứ ghi. Làm hết cả 3 phần rồi mới báo Claude chấm **một lần**.

---

## Phần A: một luật lọc (8 câu)

Dữ liệu dùng cho cả phần A:
```python
dieu_kien = {"gt": ["lang_count", 3]}
metadata  = {"lang": "vi", "lang_count": 5, "year": 2019}
```

**A1.** Luật này có 3 mảnh. Ghi ra **từng mảnh là giá trị gì** (chép đúng chuỗi/số), và mỗi mảnh có vai trò gì
(làm phép gì / nhìn dòng nào / so với cái gì).
>
phép gt bhìn vào lang count so voíw 3

**A2.** Nói luật này thành **một câu bảo vệ nói** (tiếng Việt, không có chữ `gt`).
>
nhìn dòng lang_count trên thẻ phải lớn hơn 3

**A3.** Viết biểu thức lấy ra **tên phép** từ `dieu_kien`. Nó ra gì? Vì sao trong ngoặc cuối là `[0]` mà không phải `[1]`?
>
phep = list(dieu_kien.keys())[0]
**A4.** Viết biểu thức lấy ra `"lang_count"`, và biểu thức lấy ra `3`. Cả hai **chỉ được dùng `dieu_kien`** hoặc biến `phep`.
> = phep[0]

dieu_kien[phep][0]
dieu_kien[phep][1]


**A5.** Viết biểu thức lấy ra **giá trị thật trên thẻ**. Nó ra số mấy?
Trong 4 biểu thức ở A3, A4, A5, **đúng mấy cái** có chữ `metadata`? Vì sao chỉ có từng đó?
> metadata[list[metadata.keys[1]][1]] lấy ra số 3 

**A6.** Viết dòng so sánh cho luật này, thẻ bên trái. Nó ra `True` hay `False`?
>

**A7.** Một bạn viết:
```python
ten_truong = list(metadata.keys())[1]
```
Với `metadata` ở trên nó ra gì? Nó sai ở **ý** nào (không phải sai cú pháp)? Đổi thẻ thành
`{"year": 2019, "lang_count": 5, "lang": "vi"}` thì dòng đó ra gì, và phép so sánh thành ra so cái gì với cái gì?
>

**A8.** Một bạn viết:
```python
ket_qua = isinstance(gia_tri_the, gia_tri)
```
Chuyện gì xảy ra khi chạy? `isinstance` dùng để hỏi **câu gì**? Dấu `>` hỏi **câu gì**?
>

---

## Phần B: Cặp 14, phần tử trước `in` và cả list sau `in` (5 câu)

```python
bo_loc = [{"eq": ["lang", "vi"]}, {"gt": ["year", 2020]}, {"lt": ["lang_count", 9]}]
```

**B1.** Trong `for luat in bo_loc:`, cái nào là list, cái nào là dict? Vòng lặp chạy **mấy lượt**?
>

**B2.** Điền bảng (đủ số dòng bằng số lượt):

| lượt | `luat` bằng | `list(luat.keys())[0]` |
|---|---|---|
|  |  |  |

>

**B3.** Dòng `bo_loc.keys()` chạy ra gì? Vì sao?
>

**B4.** Hai đoạn dưới **in ra khác nhau chỗ nào**? (số dòng, có ngoặc vuông hay không)
```python
# đoạn 1
for luat in bo_loc:
    print(list(luat.keys())[0])

# đoạn 2
ten = []
for luat in bo_loc:
    ten.append(list(luat.keys())[0])
print(ten)
```
>

**B5.** Sáng nay bạn nói *"`q.keys()` ra `["cam","xoai","oi"]`"*. Giải thích bằng lời: câu đó sai ở chỗ **tưởng `q` là cái gì**, còn thực ra `q` là cái gì?
>

---

## Phần C: các mẩu nhỏ trong ngày (4 câu)

```python
the = {"lang": "vi", "year": 2021}
```

**C1.** `"vi" in the` ra gì? `"lang" in the` ra gì? Vì sao khác nhau?
> false lang kia thì true

**C2.** `the["tenant"]` và `the.get("tenant")` khác nhau ra sao khi chạy?
Khi lọc chunk thật, metadata có thể **thiếu** trường. Theo bạn nên dùng cái nào, vì sao?
>

**C3.** `["year", 2020]` có mấy ô, đánh số thế nào? `list({"gt": [...]}.keys())` có mấy ô?
Vì sao cùng viết `[1]` mà một cái ra số, một cái sập?
>

**C4.** Trong code tối nay có dòng `dieu_kien[phep]` (không nháy) và dòng cũ `dieu_kien["lt"]` (có nháy).
Nếu viết `dieu_kien["phep"]` (có nháy) thì chuyện gì xảy ra, vì sao?
>
