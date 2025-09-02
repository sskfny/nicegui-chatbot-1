"""OCR stub tool: runs if attachments present."""
import asyncio
from typing import AsyncGenerator, List

async def run_ocr_stub(attachments: List[str]) -> AsyncGenerator[str, None]:
    """Yield OCR results as streaming output."""
    if not attachments:
        return
    for i, att in enumerate(attachments):
        await asyncio.sleep(0.5)
        yield f"OCR result for {att}: [stub text]"
