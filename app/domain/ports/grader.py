from typing import Protocol


class Grader(Protocol):
    def grade(self, query: str, docs: list[str]) -> list[bool]:
        ...
