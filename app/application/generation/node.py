from app.application.generation.decision import decide


def make_grade_node(grader, correct_threshold=0.6, incorrect_threshold=0.0):
    def grade_node(state):
        query = state["query"]
        docs = state["retrieved_docs"]

        grades = grader.grade(query, docs)
        verdict = decide(grades, correct_threshold, incorrect_threshold)
        attempts = state.get("attempts", 0)

        ket_qua = {"verdict": verdict, "grades": grades, "attempts": attempts + 1}

        if verdict == "INCORRECT":
            ket_qua["candidate_k"] = state.get("candidate_k", 0) * 2
        return ket_qua
    return grade_node

def make_retrieve_node(retriever, doc_store, candidate_k, top_k):
    def retrieve_node(state):
        tenant_id = state.get("tenant_id")
        query = state.get("query")
        effective_k = state.get("candidate_k", candidate_k)
        candidate_docs = retriever.search(tenant_id, query , effective_k, top_k)

        docs= []
        for doc_id, score in candidate_docs:
            text = doc_store.get(tenant_id, doc_id)
            docs.append(text)
        return {
            "retrieved_docs": docs,
            "candidate_k": effective_k,
        }
    return retrieve_node


def make_generate_node(generator):
    def generate_node(state):
        query = state["query"]
        docs = state["retrieved_docs"]

        answer = generator.generate(query, docs)

        return {"answer": answer}

    return generate_node