from typing import Optional


def reciprocal_rank_fusion(
    ranked_lists: list[list[str]], k: int = 60, top_k: Optional[int] = None
) -> list[tuple[str, float]]:
    # TODO:
    # 1. `ranked_lists` là list của nhiều danh sách doc_id đã xếp hạng (mỗi danh sách:
    #    phần tử đầu = hạng 1, phần tử thứ 2 = hạng 2, ...). Ví dụ:
    #    [["doc2", "doc1", "doc3"], ["doc1", "doc3", "doc2"]]
    # 2. Với MỖI danh sách trong ranked_lists, MỖI doc trong đó: cộng dồn
    #    1/(k + rank) vào 1 dict tổng điểm theo doc_id (rank tính từ 1, không phải 0 -
    #    coi chừng off-by-one, xem pattern table trong bug-log.md).
    #    Doc không xuất hiện trong 1 danh sách nào đó thì bỏ qua danh sách đó cho doc này,
    #    không tự bịa ra rank.
    # 3. Sort dict đó giảm dần theo điểm, cắt top_k nếu có truyền vào (None = lấy hết).
    scores: dict[str, float] = {}
    for ranked_list in ranked_lists:
        for rank, doc_id in enumerate(ranked_list, start=1):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1 / (k + rank)
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    if top_k is not None:
        ranked = ranked[:top_k]
    return ranked
