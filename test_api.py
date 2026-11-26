"""main.py 的接口测试。"""

import main
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_returns_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_chat_requires_question():
    r = client.post("/chat", json={})
    assert r.status_code == 422


def test_chat_returns_answer(monkeypatch):
    monkeypatch.setattr(
        main, "ask",
        lambda question, system="": {"answer": "mock answer", "consume": 1},
    )
    r = client.post("/chat", json={"question": "什么是RAG"})
    assert r.status_code == 200
    assert r.json()["answer"] == "mock answer"