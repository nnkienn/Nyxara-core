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
        # chỉ chốt khi temp ĐÃ CÓ CHỮ — nếu không, văn bản mở đầu bằng dấu tách sẽ sinh ra
        # một chunk không chứa chữ nào (vector của khoảng trắng, vẫn chiếm chỗ trong kho)
        if part == sep and temp.strip():
            ghep.append(temp)
            temp =""
    # 3. hết vòng lặp, tam còn chữ thì chốt nốt
    if temp:
        # phần sót không có chữ (vd đuôi "\n") thì dán vào chunk trước, đừng đứng riêng
        if temp.strip() or not ghep:
            ghep.append(temp)
        else:
            ghep[-1] += temp
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

def recursive_chunk(text: str, size: int, separators: list[str] = None) -> list[str]:
    if separators is None:
        separators = ["\n\n", "\n", " "]
    pieces = split_by_separators(text,size,separators)
    return merge_pieces(pieces,size)
