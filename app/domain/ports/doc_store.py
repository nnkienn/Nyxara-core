from typing import Protocol


class DocStore(Protocol):
    def save(self, tenant_id: str, doc_id: str, text: str) -> None:
        ...

    def get(self, tenant_id: str, doc_id: str) -> str:
        ...
    def delete(self, tenant_id: str, doc_id: str) -> None:
        ...