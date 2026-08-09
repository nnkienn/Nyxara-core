def make_retrieve_node(retriever, doc_store, candidate_k, top_k):
    def retrieve_node(state):
        tenant_id = state.get("tenant_id")
        query = state.get("query")
        candidate_docs = retriever.search(tenant_id, query , candidate_k, top_k)

        docs= []
        for doc_id, score in candidate_docs:
            text = doc_store.get(tenant_id, doc_id)
            docs.append(text)
        return {
            "retrieved_docs": docs
        }
    return retrieve_node