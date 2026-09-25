# Trace `merge_pieces` bằng tay — 2026-09-10

> Được nhìn code [recursive_chunker.py](../../app/application/chunking/recursive_chunker.py).
> **Không chạy.** Điền hết rồi mới báo Claude sửa — sai cũng cứ điền, tắc ô nào để trống ô đó.

```python
merge_pieces(["Toi", "an", "com", "roi", "di", "ngu"], size=6)
```

## Vòng 1 (mẫu)
- `piece` (món tới):                                   "Toi"
- `current_merge` TRƯỚC (thùng trước):                 ""
- `len(current_merge) + len(piece) <= size` (vừa?):    0 + 3 = 3 <= 6 → True
- chạy dòng:                                           30
- `current_merge` SAU (thùng sau):                     "Toi"
- `merges` SAU (xe sau):                               []

## Vòng 2
- `piece` (món tới): "an"
- `current_merge` TRƯỚC (thùng trước): “Toi”
- `len(current_merge) + len(piece) <= size` (vừa?): 3 + 2 <=6
- chạy dòng:
- `current_merge` SAU (thùng sau): "Toian"
- `merges` SAU (xe sau):[]

## Vòng 3
- `piece` (món tới):"com"
- `current_merge` TRƯỚC (thùng trước): "Toian"
- `len(current_merge) + len(piece) <= size` (vừa?): 5 + 3 >=8 rơi vào nhánh else
- chạy dòng:
- `current_merge` SAU (thùng sau): "com"
- `merges` SAU (xe sau): [Toian]

## Vòng 4
- `piece` (món tới): roi
- `current_merge` TRƯỚC (thùng trước): "com" 
- `len(current_merge) + len(piece) <= size` (vừa?): = 6 nhảy và dòng if 
- chạy dòng:
- `current_merge` SAU (thùng sau):"comroi"
- `merges` SAU (xe sau):[Toian]

## Vòng 5
- `piece` (món tới): "di"
- `current_merge` TRƯỚC (thùng trước): "comroi"
- `len(current_merge) + len(piece) <= size` (vừa?): 6+ 2 = 8 rơi vào nhánh else
- chạy dòng:
- `current_merge` SAU (thùng sau): "di"
- `merges` SAU (xe sau):[Toiandi]

## Vòng 6
- `piece` (món tới): "ngu"
- `current_merge` TRƯỚC (thùng trước): "di"
- `len(current_merge) + len(piece) <= size` (vừa?): 5 roi vào nhánh if 
- chạy dòng:
- `current_merge` SAU (thùng sau): "dingu"
- `merges` SAU (xe sau): [Toiandi]

## Hết vòng `for` (dòng 35 → 36)
- `current_merge` (thùng còn trên tay): "dingu"
- `if current_merge:` → True hay False: true
- `merges` SAU (xe sau): [Toiandi]

## Kết quả `return merges`:
