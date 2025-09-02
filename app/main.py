"""NiceGUI Chatbot main entrypoint."""
import asyncio
from nicegui import app, ui
from app.global_config import get_config, reload_config, mask_secrets
from app.logging_setup import logger
from app.telemetry import setup_otel
from app.tracing.langfuse_integration import langfuse
from app.auth import setup_auth_routes
from app.ui.components.header import render_header
from app.ui.components.footer import render_footer
from app.ui.components.side_panel import render_side_panel
from app.ui.components.chat_panel import render_chat_panel
from app.ui.components.response_panel import render_response_panel
from app.ui.components.thoughts_panel import render_thoughts_panel
from app.ui.components.tool_selector import render_tool_selector
from app.ui.components.metrics_panel import render_metrics_panel

# Setup telemetry
setup_otel()

# Setup authentication routes
setup_auth_routes()

@ui.page("/")
def main_page():
    """Main chat UI page."""
    render_header()
    with ui.row().classes("w-full justify-center"):
        with ui.column().classes("items-center w-2/3"):
            render_chat_panel()
            render_response_panel()
        render_metrics_panel()  # Unused, but included
    render_footer()

@ui.page("/admin/reload")
def reload_page():
    """Hot reload config page."""
    cfg = reload_config()
    ui.label("Config reloaded.")
    ui.json(mask_secrets(cfg))

def _run():
    logger.info("Starting NiceGUI Chatbot...")
    app.run(port=8080, title=get_config().get("service_name", "NiceGUI Chatbot"))

if __name__ == "__main__":
    _run()

def __mp_main__():
    _run()
