import re 

def fixed_size_chunk(text: str, size: int, overlap: int) -> list[str]:
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
    mau = "(" + re.escape(sep)+")"
    parts = re.split(mau,text)
    ghep = []
    temp = ""
    for part in parts:
        # 1. gom part vào tam
        temp+=part
        # 2. nếu part chính là sep  ->  chốt tam vào ghep, rồi cho tam về rỗng
        if (part == sep) :
            ghep.append(temp)
            temp =""
    # 3. hết vòng lặp, tam còn chữ thì chốt nốt
    if temp:
        ghep.append(temp)
    parts = ghep
    result = []
    for part in parts:
        if len(part) > size:
            result.extend(split_by_separators(part, size, separators[1:]))
        else:
            result.append(part)
    return result
def merge_pieces(pieces: list[str], size:int) -> list[str]:
    merges = []
    current_merge = ""    
    for piece in pieces:
        if (len(current_merge) + len(piece) <= size):
            current_merge += piece
        else:
            if current_merge:
                merges.append(current_merge)
            current_merge = piece
    if current_merge:
        merges.append(current_merge)
    return merges

