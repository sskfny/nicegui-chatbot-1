"""Langfuse integration (safe no-op if not configured)."""
from typing import Any, Optional
from loguru import logger
from app.global_config import get_config

class LangfuseClient:
    """Safe Langfuse client wrapper."""
    def __init__(self) -> None:
        cfg = get_config()
        self.host = cfg.get("langfuse_host")
        self.public_key = cfg.get("langfuse_public_key")
        self.secret_key = cfg.get("langfuse_secret_key")
        self.enabled = bool(self.host and self.public_key and self.secret_key)
        if self.enabled:
            logger.info(f"Langfuse enabled: {self.host}")
        else:
            logger.info("Langfuse disabled.")

    def trace_event(self, event: str, data: Optional[Any] = None) -> None:
        """Send event to Langfuse (no-op if not enabled)."""
        if not self.enabled:
            return
        # Real implementation would send to Langfuse API
        logger.debug(f"Langfuse event: {event} | {data}")

langfuse = LangfuseClient()
