"""Footer component."""
from nicegui import ui

def render_footer() -> None:
    """Render the app footer."""
    with ui.footer().classes("bg-gray-100 text-gray-600 p-2 flex items-center justify-center"):
        ui.label("© 2025 NiceGUI Chatbot | MIT License")
