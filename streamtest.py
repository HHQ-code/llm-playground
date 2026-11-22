import os
import json
import time
import httpx
api_key=os.getenv("LLM_api_key")
basic_ur1=os.getenv("LLM_ur1","https://api.deepseek.com").rstrip("/")
model=os.getenv("LLM_model","deepseek-chat")
ur1=f"{basic_ur1}/chat/completions"
t0=time.perf_counter()
first_token_at = None
chunk_count=0
if not api_key:
    raise SystemExit("没有找到LLM_api_key")
headers={
    "Authorization":f"Bearer {api_key}",
    "Content-Type":"application/json"
}
payload={
    "model":model,
    "messages":[
        {"role":"system","content":"你是一个简洁的回复助手"},
        {"role":"user","content":"什么是RAG"}
    ],
    "stream":True,
    "temperature":0.7,
    "max_tokens":200
}
with httpx.stream("post",ur1,headers=headers,json=payload,timeout=60.0)as resp:
    if resp.status_code!=200:
        resp.raise_for_status()
    for line in resp.iter_lines():
        if not line.startswith("data:"):
            continue
        raw=line[len("data:"):].strip()
        if raw == "[DONE]":
            break
        
        chunk=json.loads(raw)
        chunk_count+=1
        delta=chunk["choices"][0].get("delta",{})
        text=delta.get("content")or""
        if text:
            if first_token_at is None:
                first_token_at = time.perf_counter() - t0
            print(text,end="",flush=True)
print(f"共收到{chunk_count} 个chunk")
if first_token_at is not None:
    print(f"首token延迟:{first_token_at}")
    print(f"总耗时:{time.perf_counter() - t0}")



     

