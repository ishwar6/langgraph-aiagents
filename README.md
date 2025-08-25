# Multi-Agent Knowledge Workflow


## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install requirements:

```bash
pip install -r req.txt
```

3. Provide an OpenAI API key:

```bash
export OPENAI_API_KEY=your_key
```

4. Start the service:

```bash
uvicorn workflow.app:app
```

## Endpoints

- `POST /upload` – send a text file to extend the knowledge base.
- `GET /query?question=` – retrieve an answer and summary. Responses with low confidence are marked for human attention.


## Architecture

The workflow orchestrates four agents:

- a loader that reads and chunks documents
- an embedder that stores vectors in Chroma
- a query agent that performs retrieval and reasoning
- a summariser that condenses the context

When similarity falls below a threshold, a placeholder response signals that a human should review the query.

