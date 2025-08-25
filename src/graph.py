"""Agent workflow graph."""
from typing import List, TypedDict
from langgraph.graph import StateGraph, START, END
from agents.query import QueryAgent
from agents.summarizer import SummarizerAgent
from agents.human import human_response

class GraphState(TypedDict, total=False):
    question: str
    docs: List[str]
    answer: str
    summary: str
    needs_human: bool

def create_graph(query_agent: QueryAgent, summarizer: SummarizerAgent):
    """Builds the collaborative agent graph."""
    def query_node(state: GraphState) -> GraphState:
        docs, answer, needs_human = query_agent.run(state["question"])
        return {"docs": [d.page_content for d in docs], "answer": answer, "needs_human": needs_human}

    def summarize_node(state: GraphState) -> GraphState:
        summary = summarizer.run(state["docs"])
        return {"summary": summary}

    def human_node(state: GraphState) -> GraphState:
        return {"answer": human_response(state["question"])}

    graph = StateGraph(GraphState)
    graph.add_node("query", query_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("human", human_node)
    graph.add_edge(START, "query")
    graph.add_conditional_edges("query", lambda s: "human" if s["needs_human"] else "summarize")
    graph.add_edge("summarize", END)
    graph.add_edge("human", END)
    return graph.compile()
