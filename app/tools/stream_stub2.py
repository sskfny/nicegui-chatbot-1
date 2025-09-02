"""Stream stub 2: simulates long-running tool with streaming output."""
import asyncio
from typing import AsyncGenerator

async def run_stream_stub2(query: str) -> AsyncGenerator[str, None]:
    """Yield streaming output line by line."""
    for i in range(3):
        await asyncio.sleep(0.6)
        yield f"StreamStub2 output chunk {i+1}"
