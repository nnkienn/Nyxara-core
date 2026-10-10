# Drill 07/10 tối — port / adapter (câu 10.11), bản thu nhỏ không có Qdrant.
from typing import Protocol


# PORT = hợp đồng: kho nào cũng phải có find(word) -> list[str]
class Store(Protocol):
    def find(self, word: str) -> list[str]: ...


# ADAPTER 1: kho là list
class ListStore:
    def __init__(self):
        self.docs = ["luật đất đai", "luật thuế", "nghị định xe máy"]

    def find(self, word):
        return [d for d in self.docs if word in d]


# ADAPTER 2: kho là dict
class DictStore:
    def __init__(self):
        self.docs = {1: "luật đất đai", 2: "luật thuế", 3: "nghị định xe máy"}

    def find(self, word):
        return [d for d in self.docs.values() if word in d]


# ===== BẠN GÕ Ở ĐÂY: ADAPTER 3 — class TupleStore =====
# kho là tuple: ("luật đất đai", "luật thuế", "nghị định xe máy")
# phải có __init__ (cất tuple vào self.docs) + find(self, word) giữ đúng hợp đồng

class TupleStore:
    def __init__(self):
        self.docs = ("luật đất đai", "luật thuế", "nghị định xe máy")

    def find(self, word):
        return [d for d in self.docs if word in d]


# ===== HẾT CHỖ GÕ =====


# NGƯỜI DÙNG KHO — KHÔNG ĐƯỢC SỬA
def answer(store: Store):
    return store.find("luật")


print("ListStore :", answer(ListStore()))
print("DictStore :", answer(DictStore()))
print("TupleStore:", answer(TupleStore()))
