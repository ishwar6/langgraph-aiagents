from langgraph.graph import StateGraph, END
from .search import google_search
from .summarizer import Summarizer

def create_graph(model: str = "gpt-3.5-turbo"):
    summarizer = Summarizer(model)
    def search_node(state: dict):
        state["sources"] = google_search(state["question"])
        return state
    def answer_node(state: dict):
        state["answer"] = summarizer.run(state["question"], state["sources"])
        return state
    graph = StateGraph(dict)
    graph.add_node("search", search_node)
    graph.add_node("answer", answer_node)
    graph.add_edge("search", "answer")
    graph.add_edge("answer", END)
    graph.set_entry_point("search")
    return graph.compile()
