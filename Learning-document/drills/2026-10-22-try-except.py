# Drill try/except — 22/10 (CARE, trước khi làm nhánh đơn sai của parse_tool_call)
# Chạy: ~/My-project/Nyxara-core/.venv/bin/python Learning-document/drills/2026-10-22-try-except.py
import json

chuoi_tot = '{"query": "giá châm cứu"}'
chuoi_hong = '{invalid'

# Ô 1: chạy thử như sau, KHÔNG có try/except — xem nổ gì (đọc dòng cuối traceback)
print(json.loads(chuoi_tot))
# Ô 2: viết lại dòng json.loads(chuoi_hong) bên trong try/except:
#   - nếu đọc được  → print dict
#   - nếu nổ lỗi    → print("chuỗi hỏng") thay vì nổ
# (xoá dòng print(json.loads(chuoi_hong)) ở ô 1 khi làm ô 2)
try:
    print(json.loads(chuoi_hong))
except json.JSONDecodeError:
    print("chuỗi hỏng")