"""Embedder backed by a Chroma vector store.

This agent converts text fragments into vector representations and
persists them so that future queries can be answered through similarity
search.
"""
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

class EmbeddingAgent:
    """Persist and retrieve vector embeddings."""

    def __init__(self, collection: str = "documents") -> None:
        """Initialise the embedding model and storage backend.

        Parameters
        ----------
        collection: str
            Name of the vector collection.
        """
        self.embeddings = OpenAIEmbeddings()
        self.store = Chroma(collection_name=collection, embedding_function=self.embeddings)

    def add(self, texts: List[str]) -> None:
        """Add a batch of text fragments to the store.

        Parameters
        ----------
        texts: List[str]
            Content produced by the loader.
        """
        self.store.add_texts(texts)

    def search(self, query: str, k: int = 4):
        """Retrieve documents most relevant to a query.

        Parameters
        ----------
        query: str
            Natural language prompt.
        k: int
            Number of results to return.

        Returns
        -------
        list
            Matched documents paired with similarity scores.
        """
        return self.store.similarity_search_with_score(query, k=k)
