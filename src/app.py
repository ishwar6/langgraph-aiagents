"""FastAPI interface for the agent workflow."""
from pathlib import Path
import tempfile
from fastapi import FastAPI, UploadFile, File
from agents.loader import load_and_chunk
from agents.embedder import EmbeddingAgent
from agents.query import QueryAgent
from agents.summarizer import SummarizerAgent
from graph import create_graph

app = FastAPI()
embedder = EmbeddingAgent()
query_agent = QueryAgent(embedder)
summarizer = SummarizerAgent()
workflow = create_graph(query_agent, summarizer)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    """Ingests a document into the vector store."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        data = await file.read()
        tmp.write(data)
        path = Path(tmp.name)
    chunks = load_and_chunk(str(path))
    embedder.add(chunks)
    return {"status": "ok"}

@app.get("/query")
async def query(question: str):
    """Queries the knowledge base."""
    result = workflow.invoke({"question": question})
    return {"answer": result.get("answer"), "summary": result.get("summary"), "needs_human": result.get("needs_human")}
