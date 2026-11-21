"""大模型调用的统一封装。协议相关的字符串只出现在这个文件里。"""

import os
import httpx

BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com").rstrip("/")
MODEL = os.getenv("LLM_MODEL", "deepseek-chat")


def chat(messages: list, **options) -> dict:
    """发送 messages，返回完整响应 dict。"""
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise RuntimeError('请先设置 $env:LLM_API_KEY="sk-..."')

    payload = {"model": MODEL, "messages": messages, **options}
    headers = {"Authorization": f"Bearer {api_key}"}
    url = f"{BASE_URL}/chat/completions"

    resp = httpx.post(url, headers=headers, json=payload, timeout=60.0)
    resp.raise_for_status()
    return resp.json()


def ask(question: str, system: str = "你是一个简洁的技术助手") -> dict:
    """问一句话，直接返回答案文本。"""
    data = chat([
        {"role": "system", "content": system},
        {"role": "user", "content": question},
    ], temperature=0.7, max_tokens=200)
    
    return {"answer":data["choices"][0]["message"]["content"],
            "consume":data["usage"]["total_tokens"]
            }