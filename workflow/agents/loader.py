"""Utilities for ingesting source documents and producing chunks.

The loader reads raw text from disk using LangChain helpers and splits
it into manageable pieces ready for embedding or other downstream work.
"""
from typing import List
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_chunk(path: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """Load a file and break it into overlapping segments.

    Parameters
    ----------
    path: str
        Location of the text file on disk.
    chunk_size: int
        Target size for each chunk.
    chunk_overlap: int
        Number of characters shared between neighbours.

    Returns
    -------
    List[str]
        Collection of text fragments extracted from the document.
    """
    loader = TextLoader(path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks = splitter.split_documents(documents)
    return [c.page_content for c in chunks]
