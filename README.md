# LLM Playground

学习大模型应用开发的第一批代码：不依赖 SDK，手写 httpx 调用 `chat/completions`。

## 目录

- `llm_client.py` — 封装的调用模块，对外提供 `chat()` 和 `ask()`
- `demo1.py` / `demo2.py` — 调用示例
- `practice1.py` — 封装练习版
- `test1.py` ~ `test3.py` — 从零到跑通的演进过程

## 运行

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install httpx
$env:LLM_API_KEY = "sk-..."
python demo1.py

## 技术要点

- 直接 POST `https://api.deepseek.com/chat/completions`
- `Authorization: Bearer <key>` 认证
- 从 `choices[0].message.content` 取答案
- `usage` 里含 token 用量，可算成本