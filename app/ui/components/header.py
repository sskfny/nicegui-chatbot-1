"""Header component."""
from nicegui import ui

def render_header() -> None:
    """Render the app header."""
    with ui.header().classes("bg-blue-600 text-white p-2 flex items-center justify-between"):
        ui.image("/assets/qwen3-banner.svg").classes("h-8 mr-2")
        ui.label("NiceGUI Multi-Agent Chatbot").classes("text-lg font-bold")
        ui.button("Reload Config", on_click=lambda: ui.open("/admin/reload")).props("flat")
