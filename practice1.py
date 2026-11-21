import os
import httpx
basic_ur1=os.getenv("LLM_api_ur1","https://api.deepseek.com").rstrip("/")
model=os.getenv("LLM_model","deepseek-chat")
def chat(messages:list,**options) ->dict:
    api_key=os.getenv("LLM_api_key")
    if not api_key:
        print("请输入:$env:LLM_api_key=")
        raise SystemExit()
    ur1=f"{basic_ur1}/chat/completions"
    headers={
        "Authorization":f"Bearer {api_key}"
    }
    payload={
        "model":model,
        "messages":messages,
        **options
    }
    resp=httpx.post(ur1,headers=headers,json=payload,timeout=60.0)
    return resp.json()
def ask(question:str,system="你是一个简洁的回答助手")->str:
  data=chat([
        {"role": "system", "content": system},
        {"role": "user", "content": question},
    ], temperature=0.7, max_tokens=200)
  return data["choices"][0]["message"]["content"]
