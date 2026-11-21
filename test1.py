import json
import os
import time

import httpx

my_api_key = os.environ.get("LLM_API_KEY")
if not my_api_key:
    raise SystemExit("找不到 LLM_API_KEY，请先设置 $env:LLM_API_KEY")

my_url = os.environ.get("LLM_BASE_URL", "https://api.deepseek.com").rstrip("/")
model = os.environ.get("LLM_MODEL", "deepseek-chat")

payload = {
    "model": model,
    "messages": [
        {"role": "system", "content": "你是一个简洁的回复体，回复不超过三句话"},
        {"role": "user", "content": "用一句话解释什么是 RAG"},
    ],
    "temperature": 0.7,
    "max_tokens": 200,
}

headers = {
    "Authorization": f"Bearer {my_api_key}",
    "Content-Type": "application/json",
}

url = f"{my_url}/chat/completions"
print("POST", url)

t0 = time.perf_counter()
resp = httpx.post(url, headers=headers, json=payload, timeout=60.0)
endtime = time.perf_counter() - t0

print(f"状态码: {resp.status_code}")
print(f"总耗时: {endtime:.2f}s")

if resp.status_code != 200:
    print("请求失败")
    print(resp.text)
    resp.raise_for_status()

data = resp.json()
print("完整响应 JSON:")
print(json.dumps(data, ensure_ascii=False, indent=2))

choice = data["choices"][0]
print("答案:", choice["message"]["content"])

usage = data["usage"]
print("本次消耗:", usage["prompt_tokens"], "+", usage["completion_tokens"], "=", usage["total_tokens"])