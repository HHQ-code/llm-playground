"""异步并发实验：串行 vs asyncio.gather。"""

import asyncio
import os
import time

import httpx

BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com").rstrip("/")
MODEL = os.getenv("LLM_MODEL", "deepseek-chat")


async def ask_async(client: httpx.AsyncClient, question: str) -> str:
    """异步版 ask：复用传入的 client。"""
    api_key = os.getenv("LLM_API_KEY")
    resp = await client.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": question}],
            "max_tokens": 100,
        },
        timeout=60.0,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


async def main():
    questions = [f"用一句话解释第 {i} 个 AI 概念" for i in range(1, 11)]

    async with httpx.AsyncClient() as client:

        # ① 串行
        t0 = time.perf_counter()
        for q in questions:
            await ask_async(client, q)
        serial = time.perf_counter() - t0

        # ② 并发
        t0 = time.perf_counter()
        results = await asyncio.gather(*[ask_async(client, q) for q in questions])
        concurrent = time.perf_counter() - t0

    print(f"串行耗时: {serial:.2f}s")
    print(f"并发耗时: {concurrent:.2f}s")
    print(f"提速: {serial / concurrent:.1f}x")
    print(f"拿到 {len(results)} 个回答")


asyncio.run(main())