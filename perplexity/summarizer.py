from langchain_openai import ChatOpenAI

class Summarizer:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model=model)
    def run(self, question: str, sources):
        lines = [f"{i+1}. {s['title']} {s['link']} {s['snippet']}" for i, s in enumerate(sources)]
        prompt = question + "\n" + "\n".join(lines) + "\nAnswer with citations"
        return self.llm.invoke(prompt).content
