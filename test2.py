import os
import json
import time
import httpx
api_key=os.getenv("LLM_api_key")
basic_ur1=os.getenv("LLM_basic_ur1","https://api.deepseek.com")
basic_model=os.getenv("basic_model","deepseek-chat")
if not api_key:
    print("没有找到api_key","请输入:$env:LLM_api_key=")
    raise SystemExit()
paylode={
    "model":basic_model,
    "messages":[{"role":"system","content":"你是一个简单的回复助手，回复不超过三句话"},
                {"role":"user","content":"什么是RAG检索"}
    ],
    "temperature":0.7,
    "max_tokens":200
}
ur1=f"{basic_ur1}/chat/completions"
print("post",ur1)
headers={
"Authorization":f"Bearer {api_key}",
"Content-Type":"application/json"
}
t0=time.perf_counter()
resp=httpx.post(ur1,headers=headers,json=paylode,timeout=60)
eltime=time.perf_counter()-t0
print(f"状态码:{resp.status_code}",f"总时间：{eltime}")
if resp.status_code !=200:
    print("运行失败\n","原因：")
    print(resp.text)
    resp.raise_for_status()
data=resp.json()
choice=data["choices"][0]
print(f"回答：{choice["message"]["content"]}")
usage=data["usage"]
print(f"用量：{usage}")
print("输入用量：",usage["prompt_tokens"])
print("输出用量：",usage["completion_tokens"])
print("总用量：",usage["total_tokens"])