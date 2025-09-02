"""Tool selector UI."""
from nicegui import ui

def render_tool_selector() -> None:
    """Render tool selector."""
    with ui.row().classes("mb-2"):
        tools = ["kb_stub", "ocr_stub", "stream_stub1", "stream_stub2"]
        for tool in tools:
            ui.button(tool.replace("_", " ").title(), on_click=lambda t=tool: ui.notify(f"Tool selected: {t}"), icon="build").classes("mr-2")
