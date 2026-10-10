results = ["46/2016/nđ-cp+6", "100/2019/nđ-cp+5", "100/2019/nđ-cp+6"]
correct = "100/2019/nđ-cp+5"
for k in [1, 2, 3]:
    top = results[:k]
    hit = 1 if correct in top else 0
    print(f"k={k} | nhìn {k} dòng đầu: {top}")
    print(f"      | có điều đúng không? {'CÓ' if hit else 'KHÔNG'} -> Hit@{k} = {hit}\n")
