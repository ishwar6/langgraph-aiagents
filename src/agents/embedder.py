"""Vector store management."""
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

class EmbeddingAgent:
    """Stores and retrieves document embeddings."""
    def __init__(self, collection: str = "documents") -> None:
        self.embeddings = OpenAIEmbeddings()
        self.store = Chroma(collection_name=collection, embedding_function=self.embeddings)

    def add(self, texts: List[str]) -> None:
        """Adds text chunks to the vector store."""
        self.store.add_texts(texts)

    def search(self, query: str, k: int = 4):
        """Retrieves documents relevant to a query."""
        return self.store.similarity_search_with_score(query, k=k)
