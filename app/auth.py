"""Authentication: Simple Auth, Keycloak/OIDC, or 404 fallback."""
from nicegui import app, ui
from app.global_config import get_config
from loguru import logger
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from typing import Callable


def setup_auth_routes(app_inst: Callable) -> None:
    """Setup /auth/* routes based on config."""
    cfg = get_config()
    simple_auth = cfg.get("simple_auth")
    keycloak_url = cfg.get("keycloak_url")
    keycloak_client_id = cfg.get("keycloak_client_id")
    keycloak_client_secret = cfg.get("keycloak_client_secret")
    keycloak_redirect_uri = cfg.get("keycloak_redirect_uri")

    if simple_auth:
        @app_inst.page("/auth/login")
        def login_page():
            def do_login():
                username = ui.query("#username").value
                password = ui.query("#password").value
                if username == simple_auth["username"] and password == simple_auth["password"]:
                    app.storage.user["auth"] = True
                    logger.info(f"Simple auth login: {username}")
                    ui.open("/")
                else:
                    ui.notify("Invalid credentials", color="negative")
            with ui.card().classes("w-96 mx-auto mt-32"):
                ui.label("Login").classes("text-xl mb-4")
                ui.input("Username", id="username")
                ui.input("Password", password=True, id="password")
                ui.button("Login", on_click=do_login)

        @app_inst.page("/auth/logout")
        def logout_page():
            app.storage.user["auth"] = False
            ui.notify("Logged out.")
            ui.open("/")

    elif keycloak_url and keycloak_client_id and keycloak_client_secret and keycloak_redirect_uri:
        @app_inst.page("/auth/login")
        def login_oidc():
            url = f"{keycloak_url}/realms/master/protocol/openid-connect/auth?client_id={keycloak_client_id}&response_type=code&redirect_uri={keycloak_redirect_uri}"
            ui.open(url)

        @app_inst.page("/auth/callback")
        def callback_oidc():
            # Real implementation: handle OIDC callback, exchange code for token
            ui.notify("OIDC callback received.")
            ui.open("/")

        @app_inst.page("/auth/logout")
        def logout_oidc():
            app.storage.user["auth"] = False
            ui.notify("Logged out.")
            ui.open("/")
    else:
        @app_inst.page("/auth/{rest:path}")
        def auth_disabled(rest: str):
            ui.label("Auth disabled.").classes("text-red-600 text-xl mt-32 mx-auto")
