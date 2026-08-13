class InMemoryDocStore:
    def __init__(self) -> None:
        self.texts: dict[str, dict[str, str]] = {}

    def save(self, tenant_id: str, doc_id: str, text: str) -> None:
        self.texts.setdefault(tenant_id, {})[doc_id] = text

    def get(self, tenant_id: str, doc_id: str) -> str:
        return self.texts[tenant_id][doc_id]
    def delete(self, tenant_id: str, doc_id: str) -> None:
        if tenant_id in self.texts and doc_id in self.texts[tenant_id]:
            del self.texts[tenant_id][doc_id]   