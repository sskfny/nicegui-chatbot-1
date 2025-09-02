"""Metrics panel (included but unused)."""
from nicegui import ui

def render_metrics_panel() -> None:
    """Render metrics panel (unused)."""
    with ui.right_drawer().classes("bg-white w-64 p-4"):
        ui.label("Metrics (unused)").classes("text-lg font-bold mb-2")
