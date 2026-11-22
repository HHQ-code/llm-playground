
import json
import os

import httpx

api_key = os.environ.get("LLM_API_KEY")
if not api_key:
    raise SystemExit('请先设置 $env:LLM_API_KEY = "sk-你的key"')

base_url = os.environ.get("LLM_BASE_URL", "https://api.deepseek.com").rstrip("/")
model = os.environ.get("LLM_MODEL", "deepseek-chat")
url = f"{base_url}/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}
messages=[{"role":"system","content":"你是一个简洁的回复助手"}]
turn=0
while True:
     user_input = input("\n你: ").strip()
     if user_input.lower() in {"q", "quit", "exit"}:
        break
     if not user_input:
        continue
     messages.append({"role":"user","content":user_input})
     payload={"model":model,"messages":messages,"temperature":0.7,"max_tokens":200}
     resp=httpx.post(url,headers=headers,json=payload,timeout=60)
     data=resp.json()
     answer=data["choices"][0]["message"]["content"]
     print("回答:",answer)
     messages.append({"role":"assistant","content":answer})
     turn+=1
     usage=data["usage"]["prompt_tokens"]
     print(f"回答:{answer}")
     print(f"进行了:{turn}轮")
     print(f"本轮用了:{usage}tokens")
     print("轮次越多,prompt_tokens越多,越贵")

     