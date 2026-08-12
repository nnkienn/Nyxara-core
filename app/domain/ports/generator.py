from typing import Protocol


class Generator(Protocol):
    def generate(self, query: str, docs: list[str]) -> str:
        ...
