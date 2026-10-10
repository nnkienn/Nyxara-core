# Drill 07/10 tối — Hit@k (lát 1). Bạn gõ ruột hàm, Claude lo dữ liệu thật sau.


def hit_at_k(results: list[list[str]], answers: list[str], k: int) -> float:
    # results[i] = các điều máy khoanh cho câu i, xếp từ điểm cao xuống thấp
    # answers[i] = điều đúng của câu i
    # trả về: điểm thi, 1 số từ 0.0 tới 1.0
    # ===== BẠN GÕ Ở ĐÂY =====
    hits = 0
    for i in range(len(results)):
        top_k = results[i][:k]
        if answers[i] in  top_k:
            hits = hits + 1
    return hits / len(results )

    # ===== HẾT CHỖ GÕ =====


# ----- ĐỀ THI NHỎ: 3 câu (giống 3 lần tìm "Lạc trôi") — KHÔNG SỬA -----
results = [
    ["son_tung", "cover", "remix"],     # câu 0: đáp án ở dòng 1
    ["cover", "remix", "son_tung"],     # câu 1: đáp án ở dòng 3
    ["cover", "remix", "karaoke"],      # câu 2: không có đáp án
]
answers = ["son_tung", "son_tung", "son_tung"]

print("Hit@1 =", hit_at_k(results, answers, 1), "  (đúng phải là 0.333...)")
print("Hit@3 =", hit_at_k(results, answers, 3), "  (đúng phải là 0.666...)")
