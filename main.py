from fastapi import FastAPI
from pydantic import BaseModel

from llm_client import ask

app = FastAPI(title="LLM Playground API")


class ChatRequest(BaseModel):
    question: str
    system: str = "你是一个简洁的技术助手"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    return ask(req.question, system=req.system)