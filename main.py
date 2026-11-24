import json
import os

import httpx
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from llm_client import ask

app = FastAPI(title="LLM Playground API")


class ChatRequest(BaseModel):
    question: str
    system: str = "你是一个简洁的技术助手"


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/chat")
def chat_endpoint(req: ChatRequest) -> dict:
    return ask(req.question, system=req.system)


def stream_answer(question: str, system: str):
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL", "https://api.deepseek.com").rstrip("/")
    model = os.getenv("LLM_MODEL", "deepseek-chat")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": question},
        ],
        "stream": True,
        "temperature": 0.7,
        "max_tokens": 500,
    }
    headers = {"Authorization": f"Bearer {api_key}"}

    with httpx.stream(
        "POST",
        f"{base_url}/chat/completions",
        headers=headers,
        json=payload,
        timeout=60.0,
    ) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line.startswith("data:"):
                continue
            raw = line[len("data:"):].strip()
            if raw == "[DONE]":
                break
            chunk = json.loads(raw)
            delta = chunk["choices"][0].get("delta", {})
            text = delta.get("content") or ""
            if text:
                yield text


@app.post("/chat/stream")
def chat_stream(req: ChatRequest):
    return StreamingResponse(
        stream_answer(req.question, req.system),
        media_type="text/plain; charset=utf-8",
    )