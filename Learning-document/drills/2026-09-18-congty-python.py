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
def dem_luot(log: list) -> dict:
    so = {}                          # b1. cuon so rong, NGOAI vong for
    for dong_chu in log:             # b2. di qua tung dong
        dong = doc_dong(dong_chu)    # b3. doc dong do ra dict
        ten = dong["user"]           # b4. moi ten user ra
        if ten in so:                # b5. NEU ten da co trong so
            so[ten] = so[ten] + 1    # b6.   tang len 1
        else:                        # b7. NGUOC LAI (chua co)
            so[ten] = 1              # b8.   dat vao so, cho 1
    return so                        # b9. tra so ve




# ─── MẨU 3 ── lượt chậm nhất là của ai ───────────────────────────
# Làm xong mẩu 2 mới làm.
#   def cham_nhat(log: list) -> str:
# Phải ra:  'binh'   (1200 ms)
# Tự nghĩ: muốn biết "chậm nhất" thì trong lúc đi qua từng dòng phải NHỚ những gì?
# ✍️ GÕ Ở ĐÂY
def cham_nhat(log: list) -> str:
    # b1. một biến max rỗng ngoài vòng for 
    max = 0
    name = {}
    # b2. đi qua từng dòng
    for dong_chu in log:     
        dong = doc_dong(dong_chu)
        
    # b3. lấy cái thời gian và tên ra
        time = dong["ms"]   
        time = int(time)      
       
    # b4. nếu thời gian lớn hơn cái max 
        if(time > max):
            max = time
            name = dong["user"]
    # b5. cập nhập max = thời gian và ghi đè cái tên kèm với max

        
    return name
    # b6. return ra cái max
