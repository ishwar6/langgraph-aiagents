"""Retrieval and reasoning agent."""
from langchain_openai import ChatOpenAI
from .embedder import EmbeddingAgent

class QueryAgent:
    """Handles retrieval and reasoning."""
    def __init__(self, embedder: EmbeddingAgent, model: str = "gpt-3.5-turbo") -> None:
        self.embedder = embedder
        self.llm = ChatOpenAI(model=model)

    def run(self, question: str, k: int = 4, threshold: float = 0.5):
        """Returns documents, answer, and confidence flag."""
        docs_scores = self.embedder.search(question, k=k)
        documents = [doc for doc, _ in docs_scores]
        scores = [score for _, score in docs_scores]
        context = "\n".join(d.page_content for d in documents)
        response = self.llm.invoke(f"Question: {question}\nContext:\n{context}")
        top = scores[0] if scores else 0.0
        return documents, str(response.content), top < threshold
