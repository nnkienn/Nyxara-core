def edit_distance(a: str, b: str) -> int:
    n = len(a) + 1          # số HÀNG  = số ký tự của a, cộng 1 (hàng viền rỗng)
    m = len(b) + 1          # số CỘT   = số ký tự của b, cộng 1 (cột viền rỗng)

    # --- tạo lưới n hàng × m cột, toàn số 0 ---
    grid = []
    for _ in range(n):          # lặp n lần -> n hàng
        row = [0] * m           # mỗi hàng là m số 0
        grid.append(row)

    # --- điền VIỀN (base case) ---
    for i in range(n):          # cột đầu: grid[i][0] = i  (biến i ký tự -> rỗng = xoá i lần)
        grid[i][0] = i
    for j in range(m):          # hàng đầu: grid[0][j] = j  (biến rỗng -> j ký tự = thêm j lần)
        grid[0][j] = j

    # --- quét từng ô bên trong (bỏ qua viền -> bắt đầu từ 1) ---
    for i in range(1, n):
        for j in range(1, m):
            # a[i-1], b[j-1] là ký tự thật đang so (lệch 1 vì có hàng/cột viền rỗng)
            cost = 0 if a[i - 1] == b[j - 1] else 1

            # 👇 ĐÂY LÀ PHẦN CỦA BẠN — điền công thức min-của-3 đường:
            right  = grid[i-1][j]   + 1
            left  = grid[i][j-1]   + 1
            diagonal  = grid[i-1][j-1] + cost
            grid[i][j] = min(right ,left,diagonal)

    return grid[n - 1][m - 1]   # ô góc dưới-phải = đáp án
