"""Chat input panel: file/image upload, paste-image, chips, embedded buttons, spinner."""
from nicegui import ui
import asyncio

async def send_message():
    ui.notify("Message sent (stub)")

async def upload_file():
    ui.notify("File uploaded (stub)")

async def paste_image():
    ui.notify("Image pasted (stub)")

def render_chat_panel() -> None:
    """Render chat input panel with upload, paste, chips, spinner."""
    streaming = ui.bind_value(False)  # True while response is streaming
    uploaded_files = []

    def on_upload(e):
        for file in e.files:
            uploaded_files.append(file.name)
        ui.refresh()

    def remove_file(name):
        uploaded_files.remove(name)
        ui.refresh()

    def open_tool_dialog():
        with ui.dialog() as dialog:
            dialog.open()
            ui.label("Select Tools").classes("text-lg font-bold mb-2")
            tools = ["kb_stub", "ocr_stub", "stream_stub1", "stream_stub2"]
            selected_tools = []
            for tool in tools:
                def select_tool(t=tool):
                    if t in selected_tools:
                        selected_tools.remove(t)
                    else:
                        selected_tools.append(t)
                    ui.refresh()
                ui.button(tool.replace("_", " ").title(), on_click=select_tool).classes("mb-2")
            ui.button("Done", on_click=dialog.close).classes("mt-4")

    with ui.card().classes("w-full p-4 flex flex-col items-center"):
        if uploaded_files:
            with ui.row().classes("mb-2"):
                for chip in uploaded_files:
                    ui.chip(chip).props("removable").on("remove", lambda e, name=chip: remove_file(name))
        chat_input = ui.input("Type your message...").props("rounded outlined").bind_enabled(lambda: not streaming.value)
        with ui.row().classes("mt-2"):
            ui.button("📎", on_click=lambda: ui.upload(on_upload)).props("flat").bind_enabled(lambda: not streaming.value)
            ui.button("Paste Image", on_click=paste_image).props("flat").bind_enabled(lambda: not streaming.value)
            ui.button("⚙️", on_click=open_tool_dialog).props("flat").bind_enabled(lambda: not streaming.value)
            ui.button("➤", on_click=send_message).props("flat").bind_enabled(lambda: not streaming.value)
        ui.spinner(size="sm", color="primary").bind_visibility(streaming)
        ui.button("Clear Current Chat History", on_click=lambda: ui.notify("History cleared (display-only)"), color="negative", icon="delete").bind_enabled(lambda: not streaming.value)
