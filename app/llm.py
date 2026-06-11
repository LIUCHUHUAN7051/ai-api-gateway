"""LLM 服务层 — 封装 DeepSeek API 调用"""

import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

DEFAULT_SYSTEM = "你是一个有用的 AI 助手。回答简洁准确，使用中文。"


def _get_client() -> OpenAI:
    """延迟初始化 OpenAI 客户端（避免构建时缺少 key 报错）"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError(
            "DEEPSEEK_API_KEY 未设置。"
            "HF Spaces: Settings → Repository secrets 添加 DEEPSEEK_API_KEY"
        )
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")


def chat_completion(
    message: str,
    system_prompt: str | None = None,
    temperature: float = 0.7,
) -> str:
    """通用对话补全"""
    client = _get_client()
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt or DEFAULT_SYSTEM},
            {"role": "user", "content": message},
        ],
        temperature=temperature,
    )
    return resp.choices[0].message.content or ""


def summarize(text: str, max_sentences: int = 5) -> str:
    """文本摘要"""
    client = _get_client()
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": (
                f"你是一个专业的文本摘要助手。请用不超过 {max_sentences} 句话概括以下内容，"
                "保留关键信息，语言简洁。"
            )},
            {"role": "user", "content": text},
        ],
        temperature=0.3,
    )
    return resp.choices[0].message.content or ""


def translate(text: str, target_language: str) -> tuple[str, str | None]:
    """翻译文本，返回 (翻译结果, 源语言)"""
    client = _get_client()
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": (
                "你是一个专业翻译助手。请将用户输入的文本翻译成指定的目标语言。"
                "先判断源语言，然后输出翻译结果。"
                "格式：\n[源语言] -> [目标语言]\n翻译内容"
            )},
            {"role": "user", "content": f"请翻译成{target_language}：\n{text}"},
        ],
        temperature=0.3,
    )
    content = resp.choices[0].message.content or ""
    lines = content.split("\n", 1)
    source_lang = None
    if "->" in lines[0]:
        source_lang = lines[0].split("->")[0].strip().strip("[]")
        translation = lines[1] if len(lines) > 1 else lines[0]
    else:
        translation = content
    return translation.strip(), source_lang


def analyze_sentiment(text: str) -> tuple[list[dict], str]:
    """情感分析，返回 (情感列表, 总体判断)"""
    client = _get_client()
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": (
                "你是一个情感分析助手。分析以下文本的情感倾向，以 JSON 格式输出：\n"
                '{"sentiments": [{"label": "正面/负面/中性", "score": 0.95}], '
                '"overall": "整体判断"}'
            )},
            {"role": "user", "content": text},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )
    import json
    content = resp.choices[0].message.content or "{}"
    try:
        data = json.loads(content)
        return data.get("sentiments", []), data.get("overall", "")
    except json.JSONDecodeError:
        return [{"label": "中性", "score": 1.0}], "无法分析"
