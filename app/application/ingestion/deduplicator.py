def dedup_exact(chunks : list[str]) ->list[str]:
    seen = set()
    result = []
    for chunk in chunks:
        if chunk in seen:
            continue
        seen.add(chunk)
        result.append(chunk)
    return result