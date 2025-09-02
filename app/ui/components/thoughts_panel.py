"""Thoughts panel: streamed tool outputs."""
from nicegui import ui

def render_thoughts_panel() -> None:
    """Render thoughts panel with streaming tool outputs."""
    with ui.card().classes("w-full p-4 mt-2"):
        ui.label("Thoughts:").classes("font-semibold mb-2")
        for thought in ["Plan: run selected tools in parallel.", "[kb_stub] Knowledge Base:", "[stream_stub1] StreamStub1 output chunk 1"]:
            ui.label(thought).classes("text-sm")
