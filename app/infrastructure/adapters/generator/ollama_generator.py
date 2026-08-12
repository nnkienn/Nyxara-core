import httpx


class OllamaGenerator:
    def __init__(self, base_url: str, model: str = "qwen2.5:3b") -> None:
        self.base_url = base_url
        self.model = model

    def generate(self, query: str, docs: list[str]) -> str:
        context = "\n\n".join(docs)
        prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer the question using ONLY the context above. If the context doesn't contain the answer, say so."
        response = httpx.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False},
            timeout=60.0,
        )
        data = response.json()
        return data["response"].strip()