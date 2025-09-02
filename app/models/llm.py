"""LLM wrapper for orchestration."""
from app.global_config import get_config
from openai import AsyncOpenAI
from typing import List

cfg = get_config()
openai_client = AsyncOpenAI(api_key=cfg["openai_api_key"], base_url=cfg["openai_base_url"])

async def call_llm(messages: List[dict], model: str = None) -> str:
    """Call LLM and return response."""
    model = model or cfg["models"]["primary"]
    response = await openai_client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False
    )
    return response.choices[0].message.content
