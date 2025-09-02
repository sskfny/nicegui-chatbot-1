"""Response panel: final LLM response display."""
from nicegui import ui

def render_response_panel() -> None:
    """Render response panel."""
    with ui.card().classes("w-full p-4 mt-2"):
        show_thinking = ui.switch("Show Thinking").classes("mb-2")
        thoughts = [
            "Plan: run selected tools in parallel.",
            "[kb_stub] Knowledge Base:",
            "[stream_stub1] StreamStub1 output chunk 1"
        ]
        thoughts_container = ui.column().classes("mb-2")
        for thought in thoughts:
            ui.label(thought).classes("text-sm")
        thoughts_container.bind_visibility(show_thinking)
        ui.label("Response:").classes("font-semibold mb-2")
        ui.label("[Final response will appear here]").classes("text-lg")
