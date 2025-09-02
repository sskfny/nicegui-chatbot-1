"""KB stub tool: returns static info."""
import asyncio
from typing import AsyncGenerator

async def run_kb_stub(query: str) -> AsyncGenerator[str, None]:
    """Yield static KB info as streaming output."""
    kb_info = [
        "Knowledge Base:",
        "- How to use the chatbot",
        "- Supported tools: KB, OCR, Streaming Stubs",
        "- Feedback and session management"
    ]
    for line in kb_info:
        await asyncio.sleep(0.3)
        yield line
