import httpx


class OllamaGrader:
    def __init__(self, base_url: str, model: str = "qwen2.5:3b") -> None:
        self.base_url = base_url
        self.model = model

    def _grade_one(self, query: str, doc: str) -> bool:
        prompt = f"Question: {query}\nPassage: {doc}\nIs the passage above relevant to the question? Answer only YES or NO."
        response = httpx.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False},
            timeout=60.0,
        )

        data = response.json()
        answer = data["response"].strip().upper()
        return answer.startswith("YES")


    def grade(self, query: str, docs: list[str]) -> list[bool]:
        results = []
        for doc in docs:
            grade = self._grade_one(query, doc)
            results.append(grade)
        return results