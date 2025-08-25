"""Context summarization agent."""
from typing import List
from langchain_openai import ChatOpenAI

class SummarizerAgent:
    """Produces a concise summary from documents."""
    def __init__(self, model: str = "gpt-3.5-turbo") -> None:
        self.llm = ChatOpenAI(model=model)

    def run(self, docs: List[str]) -> str:
        """Summarizes content from documents."""
        content = "\n".join(docs)
        result = self.llm.invoke(f"Summarize:\n{content}")
        return str(result.content)
