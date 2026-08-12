from langgraph.graph import END, StateGraph

from app.application.generation.decision import route
from app.application.generation.node import (
    make_generate_node,
    make_grade_node,
    make_retrieve_node,
)
from app.application.generation.state import CRAGeneratorState


def build_graph(retriever, doc_store, grader, generator, candidate_k=10, top_k=5, max_attempts=3):
    # TODO 1: tạo 3 node thật bằng cách gọi 3 hàm make_*_node đã xây xong, truyền đúng
    # dependency (retriever/doc_store cho retrieve, grader cho grade, generator cho generate).
    retrieve_node = make_retrieve_node(retriever, doc_store, candidate_k, top_k)    
    grade_node = make_grade_node(grader)
    generate_node = make_generate_node(generator)

    # TODO 2: viết hàm router(state) — LangGraph conditional edge chỉ nhận đúng 1 tham số
    # `state`, nhưng route() cần 3 tham số (verdict, attempts, max_attempts). Viết 1 hàm nhỏ
    # đọc state["verdict"], state["attempts"], gọi route(...) rồi trả kết quả (đúng closure
    # đã học ở retrieve_node, "nhớ" được max_attempts).
    def router(state):
        verdict = state.get("verdict", None)
        attempts = state.get("attempts", 0)
        return route(verdict, attempts, max_attempts)

    # TODO 3: tạo graph, đăng ký 3 node bằng graph.add_node("tên", hàm) — đặt tên
    # "retrieve", "grade", "generate" (khớp với path_map sẽ dùng ở TODO 5).
    graph = StateGraph(CRAGeneratorState)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("grade", grade_node)
    graph.add_node("generate", generate_node)

    # TODO 4: graph.set_entry_point(...) — node nào chạy đầu tiên?
    # graph.add_edge(...) — nối "retrieve" -> "grade" (luôn luôn, không điều kiện).
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "grade")

    # TODO 5: graph.add_conditional_edges("grade", router, {"retrieve": "retrieve",
    # "generate": "generate"}) — router trả về "retrieve" hoặc "generate" (đúng string route()
    # đã trả), path_map dịch string đó thành tên node thật (ở đây trùng tên luôn cho dễ).
    graph.add_conditional_edges("grade", router, {"retrieve": "retrieve", "generate": "generate"})
    

    # TODO 6: graph.add_edge("generate", END) — sau generate thì kết thúc.
    graph.add_edge("generate", END)
    # TODO 7: return graph.compile()
    return graph.compile()
