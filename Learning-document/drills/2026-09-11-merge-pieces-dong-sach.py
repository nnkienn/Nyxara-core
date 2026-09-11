# Mốc 1/12 — tự viết lại merge_pieces, ĐÓNG SÁCH (2026-09-11 sáng)
# - Đóng app/application/chunking/recursive_chunker.py. Tắt Copilot. Không mở git log.
# - Viết xong (hoặc tới 07:45) thì báo Claude — Claude chạy và so với bản thật.


def merge_pieces(pieces: list[str], size: int) -> list[str]:
    merges = []
    current = ""
    for piece in pieces:
        if(len(current) + len ()
