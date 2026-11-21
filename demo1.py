from llm_client import ask

result=ask("什么是 RAG")
print(result["answer"])
print(result["consume"])