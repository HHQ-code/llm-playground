import os
import time
import json
import httpx
api_key=os.getenv("LLM_api_key")
basic_ur1=os.getenv("basic_api_ur1","https://api.deepseek.com")
model=os.getenv("model","deepseek-chat")
if not api_key:
    print("没有找到api_key\n","请输入：$env:LLM_api_key")
    raise
ur1=f"{basic_ur1}/chat/completions"
headers={
    "Authorization":f"Bearer {api_key}",
    "Content-Type":"application/json"
}
paylode={
    "model":model,
    "messages":[{"role":"system","content":"你是一个回答助手，回答不超过三句话"},
                {"role":"user","content":"什么是RAG"}],
    "temperature":0.7,
    "max_tokens":200
}
resp=httpx.post(ur1,headers=headers,json=paylode,timeout=60)
if resp.status_code !=200:
    print("状态码不对")
    print(resp.text)
    resp.raise_for_status()
print(resp.status_code)
data=resp.json()
print("回答:",data["choices"][0]["message"]["content"])
t0=time.perf_counter()
eltime=time.perf_counter()-t0
print("响应时长:",f"{eltime:.2f}")

