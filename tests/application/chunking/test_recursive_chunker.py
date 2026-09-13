from app.application.chunking.recursive_chunker import (
    fixed_size_chunk,
    merge_pieces,
    recursive_chunk,
    split_by_separators,
)


def test_overlap_between_consecutive_chunks():
    chunks = fixed_size_chunk("ABCDEFGHIJ", size=6, overlap=2)

    assert chunks[0] == "ABCDEF"
    assert chunks[1] == "EFGHIJ"


def test_splits_by_paragraph_then_word():
    text = "Meo thich ngu\n\nCho thich chay"

    result = split_by_separators(text, size=10, separators=["\n\n", " "])
    assert "".join(result) == text
    assert result == ['Meo ', 'thich ', 'ngu\n\n', 'Cho ', 'thich ', 'chay']


def test_merge_pieces_gop_cac_mau_nho_toi_sat_size():
    """Ca gộp thường: nhiều mẩu bé được dồn chung cho tới khi thêm nữa là vượt size."""
    pieces = ["Meo ", "thich ", "ngu ", "nhieu"]

    assert merge_pieces(pieces, size=10) == ["Meo thich ", "ngu nhieu"]


def test_merge_pieces_chot_tui_cuoi():
    """Ca túi cuối: mẩu còn lại sau vòng lặp phải được chốt, không được rơi mất."""
    pieces = ["aaa", "bbb", "c"]

    ket_qua = merge_pieces(pieces, size=6)

    assert ket_qua == ["aaabbb", "c"]
    assert "".join(ket_qua) == "aaabbbc"


def test_mau_dai_hon_size_duoc_giu_nguyen_khong_chem_doi_tu():
    """size là TRẦN chứ không phải chỉ tiêu: gặp từ dài hơn size thì giữ nguyên từ."""
    ket_qua = recursive_chunk("motucucdaikhongcodauphancach", size=5)

    assert ket_qua == ["motucucdaikhongcodauphancach"]


def test_khong_sinh_chunk_khong_co_chu():
    """Regression: văn bản mở đầu/kết thúc bằng dấu tách từng đẻ ra chunk chỉ chứa khoảng trắng."""
    for text in (" mo dau bang khoang trang", "\n\nmo dau bang xuong dong",
                 "hai  khoang  trang  lien  nhau", "Meo thich ngu\n\nCho thich chay"):
        for size in (1, 3, 8, 20):
            chunks = recursive_chunk(text, size)

            assert all(c.strip() for c in chunks), (text, size, chunks)


def test_chunk_ghep_lai_ra_dung_van_ban_goc():
    """Lời hứa lõi của chunker: CẮT văn bản, không XOÁ ký tự nào."""
    for text in (" mo dau", "ket thuc ", "a\n\nb\n\nc", "Cau mot. Cau hai.  Cau ba.", "a b"):
        for size in (1, 3, 8, 20):
            assert "".join(recursive_chunk(text, size)) == text, (text, size)
