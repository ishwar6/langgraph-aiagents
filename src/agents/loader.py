"""Document ingestion utilities."""
from typing import List
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_chunk(path: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """Loads a document and returns text chunks."""
    loader = TextLoader(path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(documents)
    return [c.page_content for c in chunks]
