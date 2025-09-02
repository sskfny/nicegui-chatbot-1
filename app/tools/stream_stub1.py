"""Stream stub 1: simulates long-running tool with streaming output."""
import asyncio
from typing import AsyncGenerator

async def run_stream_stub1(query: str) -> AsyncGenerator[str, None]:
    """Yield streaming output line by line."""
    for i in range(5):
        await asyncio.sleep(0.4)
        yield f"StreamStub1 output chunk {i+1}"
