<div align="center">
  <br>
  <h1>⚡ AI API 网关</h1>
  <p><strong>基于 FastAPI + DeepSeek 的 AI 后端服务</strong></p>
  <br>
</div>

## ✨ 功能

| 接口 | 说明 |
|------|------|
| 💬 `POST /chat` | 通用 AI 对话，支持自定义系统提示词和温度 |
| 📝 `POST /summarize` | 文本摘要，控制摘要长度 |
| 🌍 `POST /translate` | 多语言翻译，自动检测源语言 |
| 😊 `POST /analyze-sentiment` | 情感分析，返回情感标签和置信度 |
| ❤️ `GET /health` | 健康检查 |

## 🛠️ 技术栈

```
后端框架    ─  FastAPI
AI 模型     ─  DeepSeek API (OpenAI SDK)
数据校验    ─  Pydantic v2
API 文档    ─  Swagger UI / ReDoc (自动生成)
```

## 🚀 本地运行

```bash
# 1. 克隆
git clone https://github.com/LIUCHUHUAN7051/ai-api-gateway.git
cd ai-api-gateway

# 2. 装依赖
pip install -r requirements.txt

# 3. 配置 API Key
cp .env.example .env
# 在 .env 中填入 DEEPSEEK_API_KEY=你的key

# 4. 启动
uvicorn app.main:app --reload --port 8000
```

打开浏览器访问 `http://localhost:8000/docs` 查看 Swagger API 文档。

## 📖 API 使用示例

### 对话

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "中国有多大面积？", "temperature": 0.7}'
```

### 摘要

```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "...长文本...", "max_sentences": 3}'
```

### 翻译

```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "target_language": "中文"}'
```

## 🏗️ 项目结构

```
ai-api-gateway/
├── app/
│   ├── __init__.py
│   ├── main.py       # FastAPI 应用主入口 & 路由
│   ├── schemas.py    # Pydantic 请求/响应模型
│   └── llm.py        # LLM 服务层（DeepSeek API 封装）
├── requirements.txt  # 依赖清单
├── .env.example      # API Key 模板
├── .gitignore        # Git 忽略规则
└── README.md         # 项目说明
```

## 📚 API 文档

启动服务后自动生成：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 👤 关于

- 作者：刘理鑫
- 求职方向：AI 应用开发工程师
- 邮箱：CHUIZI705179074@outlook.com
