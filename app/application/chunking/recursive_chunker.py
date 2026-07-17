def recursive_chunk(text: str, size: int, overlap: int) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


def split_by_separators(text: str, size: int, separators: list[str]) -> list[str]:
    if len(text) <= size or not separators:
        return [text]

    sep = separators[0]
    parts = text.split(sep)

    result = []
    for part in parts:
        if len(part) > size:
            result.extend(split_by_separators(part, size, separators[1:]))
        else:
            result.append(part)
    return result
