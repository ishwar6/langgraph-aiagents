from fastapi import FastAPI
from .graph import create_graph

app = FastAPI()
workflow = create_graph()

@app.get("/query")
async def query(q: str):
    result = workflow.invoke({"question": q})
    return {"answer": result.get("answer"), "sources": result.get("sources")}
