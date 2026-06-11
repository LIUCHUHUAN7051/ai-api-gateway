"""FastAPI AI API 网关 — 主应用"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import (
    ChatRequest, ChatResponse, ErrorResponse,
    SummarizeRequest, SummarizeResponse,
    TranslateRequest, TranslateResponse,
    SentimentRequest, SentimentResponse, SentimentItem,
    HealthResponse,
)
from . import llm

app = FastAPI(
    title="AI API 网关",
    description="基于 FastAPI + DeepSeek 的 AI 应用后端服务，提供对话、摘要、翻译、情感分析等能力。",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """API 根路径"""
    return {
        "service": "AI API 网关",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": [
            "GET  /health",
            "POST /chat",
            "POST /summarize",
            "POST /translate",
            "POST /analyze-sentiment",
        ],
    }


# ==================== 路由 ====================


@app.get("/health", response_model=HealthResponse, tags=["系统"])
async def health_check():
    """健康检查接口"""
    return HealthResponse()


@app.post("/chat", response_model=ChatResponse, responses={400: {"model": ErrorResponse}}, tags=["对话"])
async def chat(req: ChatRequest):
    """通用 AI 对话"""
    try:
        reply = llm.chat_completion(
            message=req.message,
            system_prompt=req.system_prompt,
            temperature=req.temperature,
        )
        return ChatResponse(reply=reply)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/summarize", response_model=SummarizeResponse, tags=["文本处理"])
async def summarize(req: SummarizeRequest):
    """文本摘要"""
    try:
        summary = llm.summarize(req.text, req.max_sentences)
        return SummarizeResponse(
            summary=summary,
            original_length=len(req.text),
            summary_length=len(summary),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/translate", response_model=TranslateResponse, tags=["文本处理"])
async def translate(req: TranslateRequest):
    """文本翻译"""
    try:
        translated, source_lang = llm.translate(req.text, req.target_language)
        return TranslateResponse(
            translated_text=translated,
            source_language=source_lang,
            target_language=req.target_language,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/analyze-sentiment", response_model=SentimentResponse, tags=["文本处理"])
async def sentiment(req: SentimentRequest):
    """情感分析"""
    try:
        sentiments, overall = llm.analyze_sentiment(req.text)
        items = [SentimentItem(**s) if isinstance(s, dict) else SentimentItem(label=s, score=1.0) for s in sentiments]
        return SentimentResponse(sentiments=items, overall=overall)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
