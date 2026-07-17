from app.application.ingestion.edit_distance import edit_distance


def test_one_substitution():
    # "beo" vs "meo" — thay 1 ký tự (b -> m). Số này bạn đã tính tay trong algorithms.md.
    assert edit_distance("beo", "meo") == 1  # ← điền số


def test_identical_strings():
    # 2 chuỗi giống hệt nhau -> không tốn phép nào.
    assert edit_distance("meo", "meo") == 0  # ← điền số


def test_one_deletion():
    # "meo" -> "eo": xoá 1 ký tự.
    assert edit_distance("meo", "eo") == 1  # ← điền số


def test_one_insertion():
    # "cat" -> "cats": thêm 1 ký tự.
    assert edit_distance("cat", "cats") == 1  # ← điền số


def test_completely_different():
    # "cat" vs "dog": không ký tự nào trùng vị trí.
    assert edit_distance("cat", "dog") == 3  # ← điền số
