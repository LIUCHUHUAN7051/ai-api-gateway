"""Pydantic 请求/响应模型"""

from pydantic import BaseModel, Field


# ===== 通用 =====

class ChatRequest(BaseModel):
    message: str = Field(..., description="用户消息", min_length=1, max_length=8000)
    system_prompt: str | None = Field(
        None, description="可选系统提示词，覆盖默认"
    )
    temperature: float = Field(0.7, ge=0, le=2, description="采样温度")


class ChatResponse(BaseModel):
    reply: str = Field(..., description="AI 回复内容")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="错误信息")
    detail: str | None = Field(None, description="详细错误")


# ===== 摘要 =====

class SummarizeRequest(BaseModel):
    text: str = Field(..., description="待摘要文本", min_length=10, max_length=10000)
    max_sentences: int = Field(5, ge=1, le=20, description="摘要句子数")


class SummarizeResponse(BaseModel):
    summary: str = Field(..., description="摘要结果")
    original_length: int = Field(..., description="原文长度（字符）")
    summary_length: int = Field(..., description="摘要长度（字符）")


# ===== 翻译 =====

class TranslateRequest(BaseModel):
    text: str = Field(..., description="待翻译文本", min_length=1, max_length=5000)
    target_language: str = Field("中文", description="目标语言，如 中文、英语、日语、法语")


class TranslateResponse(BaseModel):
    translated_text: str = Field(..., description="翻译结果")
    source_language: str | None = Field(None, description="检测到的源语言")
    target_language: str = Field(..., description="目标语言")


# ===== 情感分析 =====

class SentimentRequest(BaseModel):
    text: str = Field(..., description="待分析文本", min_length=1, max_length=5000)


class SentimentItem(BaseModel):
    label: str = Field(..., description="情感标签")
    score: float = Field(..., description="置信度 0-1")


class SentimentResponse(BaseModel):
    sentiments: list[SentimentItem] = Field(..., description="情感分析结果")
    overall: str = Field(..., description="整体判断")


# ===== 健康检查 =====

class HealthResponse(BaseModel):
    status: str = Field("ok", description="服务状态")
    version: str = Field("1.0.0", description="API 版本")
    model: str = Field("deepseek-chat", description="当前 AI 模型")
