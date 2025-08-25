"""Agent responsible for retrieval and reasoning.

It searches the vector store for context and asks a language model to
craft an answer. A simple threshold determines when a question should be
escalated for human review.
"""
from langchain_openai import ChatOpenAI
from .embedder import EmbeddingAgent

class QueryAgent:
    """Combine retrieval with language model reasoning."""

    def __init__(self, embedder: EmbeddingAgent, model: str = "gpt-3.5-turbo") -> None:
        """Configure the agent.

        Parameters
        ----------
        embedder: EmbeddingAgent
            Vector store interface.
        model: str
            Identifier for the chat model.
        """
        self.embedder = embedder
        self.llm = ChatOpenAI(model=model)

    def run(self, question: str, k: int = 4, threshold: float = 0.5):
        """Answer a question and flag low-confidence results.

        Parameters
        ----------
        question: str
            User query.
        k: int
            Number of documents to retrieve.
        threshold: float
            Maximum distance before escalation.

        Returns
        -------
        tuple
            Retrieved documents, generated answer, and escalation flag.
        """
        docs_scores = self.embedder.search(question, k=k)
        documents = [doc for doc, _ in docs_scores]
        scores = [score for _, score in docs_scores]
        context = "\n".join(d.page_content for d in documents)
        response = self.llm.invoke(f"Question: {question}\nContext:\n{context}")
        top = scores[0] if scores else 0.0
        return documents, str(response.content), top < threshold
