# ĐỀ SLOT CÔNG TY 18/09 — PYTHON THỰC TẾ: ĐỌC LOG THÀNH DICT
# Chỉ gõ vào chỗ có  ✍️ GÕ Ở ĐÂY. Tắt Copilot.
# Mỗi lần MỘT mẩu → báo Claude chạy → mới sang mẩu sau. Sai cứ để đó, chạy rồi sửa.
#
# Bài đời thường: server ghi mỗi lượt gọi API thành MỘT dòng chữ.
# Việc của bạn: biến dòng chữ thành dict, rồi trả lời 2 câu hỏi về cả đống dòng.


# ─── DỮ LIỆU (đừng sửa) ──────────────────────────────────────────
dong = "user=kien action=login ms=120"

log = [
    "user=kien action=login ms=120",
    "user=an action=search ms=340",
    "user=kien action=search ms=90",
    "user=an action=logout ms=15",
    "user=binh action=search ms=1200",
]


# ─── MẨU 1 ── một dòng chữ → dict ────────────────────────────────
# Từ biến  dong  ở trên, làm ra:  {'user': 'kien', 'action': 'login', 'ms': '120'}
# Gợi ý duy nhất: chuỗi có hàm .split(<dấu>), cắt ở đâu thì bạn quyết.
# Đặt tên hàm:  def doc_dong(dong: str) -> dict:
# ✍️ GÕ Ở ĐÂY

def doc_dong(dong:str) -> dict:
    so = {}
    for pieces in dong.split(" "):
        temp = pieces.split("=") 
        so[temp[0]] = temp[1]
    return so
        
    


# ─── MẨU 2 ── đếm: mỗi user gọi bao nhiêu lượt ───────────────────
# Làm xong mẩu 1 mới làm. Dùng lại doc_dong.
#   def dem_luot(log: list) -> dict:
# Phải ra:  {'kien': 2, 'an': 2, 'binh': 1}
# ✍️ GÕ Ở ĐÂY



# ─── MẨU 3 ── lượt chậm nhất là của ai ───────────────────────────
# Làm xong mẩu 2 mới làm.
#   def cham_nhat(log: list) -> str:
# Phải ra:  'binh'   (1200 ms)
# Tự nghĩ: muốn biết "chậm nhất" thì trong lúc đi qua từng dòng phải NHỚ những gì?
# ✍️ GÕ Ở ĐÂY

