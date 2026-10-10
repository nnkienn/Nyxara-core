# Drill 08/10 tối — gõ lại hit_at_k TỪ TRẮNG (đóng lời giải trong chat trước khi gõ).


def hit_at_k(results: list[list[str]], answers: list[str], k: int) -> float:
    # ===== BẠN GÕ Ở ĐÂY =====
    pass
    # ===== HẾT CHỖ GÕ =====


# ----- ĐỀ THI NHỎ — KHÔNG SỬA -----
results = [
    ["son_tung", "cover", "remix"],     # câu 0: đáp án ở dòng 1
    ["cover", "remix", "son_tung"],     # câu 1: đáp án ở dòng 3
    ["cover", "remix", "karaoke"],      # câu 2: không có đáp án
]
answers = ["son_tung", "son_tung", "son_tung"]

print("Hit@1 =", hit_at_k(results, answers, 1), "  (đúng phải là 0.333...)")
print("Hit@2 =", hit_at_k(results, answers, 2), "  (đúng phải là 0.333...)")
print("Hit@3 =", hit_at_k(results, answers, 3), "  (đúng phải là 0.666...)")
