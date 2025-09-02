"""Shared state for orchestration pipeline."""
from typing import List, Dict, Any

class ChatState:
    """State object for orchestration."""
    def __init__(self, user_input: str, selected_tools: List[str], attachments: List[str] = None):
        self.user_input = user_input
        self.selected_tools = selected_tools
        self.attachments = attachments or []
        self.thoughts: List[str] = []
        self.tool_outputs: Dict[str, List[str]] = {}
        self.final_response: str = ""
