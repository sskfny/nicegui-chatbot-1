"""Left drawer: tools selector, recent tools chips."""
from nicegui import ui
from typing import List

def render_side_panel() -> None:
    """Render toggleable session list with search, edit, delete, and activate actions."""
    panel_open = ui.bind_value(True)
    sessions = [
        {"id": 1, "name": "NiceGUI multi-agent frame..."},
        {"id": 2, "name": "Open-source chat framework"},
        {"id": 3, "name": "Chat GUI framework"},
    ]
    active_session = ui.bind_value(sessions[0]["id"])
    search_text = ui.bind_value("")

    def toggle_panel():
        panel_open.value = not panel_open.value

    def activate_session(session_id):
        active_session.value = session_id
        ui.notify(f"Activated session {session_id}")

    def delete_session(session_id):
        ui.notify(f"Deleted session {session_id}")
        # Remove from sessions list in real app

    def rename_session(session, new_name):
        session["name"] = new_name
        ui.notify(f"Renamed session {session['id']} to {new_name}")

    with ui.left_drawer().classes("bg-white w-72 p-4"):
        with ui.row().classes("justify-between items-center mb-2"):
            ui.label("Chats").classes("text-lg font-bold")
            ui.button("☰", on_click=toggle_panel).props("flat")
        if panel_open.value:
            ui.input("Search chats", value=search_text).props("clearable outlined dense")
            filtered_sessions = [s for s in sessions if search_text.value.lower() in s["name"].lower()]
            for session in filtered_sessions:
                with ui.row().classes("items-center mb-2"):
                    name_input = ui.input(value=session["name"]).props("dense outlined")
                    name_input.on("change", lambda e, s=session: rename_session(s, e.value))
                    ui.button("🖉", on_click=lambda s=session: name_input.focus()).props("flat")
                    ui.button("🗑️", on_click=lambda s=session: delete_session(s["id"])).props("flat")
                    ui.button("Activate", on_click=lambda s=session: activate_session(s["id"])).props("flat").bind_enabled(lambda: active_session.value != session["id"])
