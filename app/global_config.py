"""Global config loader with env substitution and hot reload."""
import json
import os
from typing import Any, Dict
from loguru import logger
from threading import Lock

_CONFIG_PATH = os.getenv("CONFIG_PATH", "config.json")
_config: Dict[str, Any] = {}
_config_lock = Lock()


def _substitute_env(value: Any) -> Any:
    if isinstance(value, str):
        return os.path.expandvars(value)
    if isinstance(value, dict):
        return {k: _substitute_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_substitute_env(v) for v in value]
    return value


def load_config() -> Dict[str, Any]:
    """Load config from file, substituting environment variables."""
    global _config
    with _config_lock:
        try:
            with open(_CONFIG_PATH, "r") as f:
                raw = json.load(f)
            _config = _substitute_env(raw)
            logger.info(f"Config loaded from {_CONFIG_PATH}")
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            _config = {}
    return _config


def get_config() -> Dict[str, Any]:
    """Get current config."""
    with _config_lock:
        return _config.copy()


def mask_secrets(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Mask secrets for display."""
    masked = cfg.copy()
    for k in ["openai_api_key", "langfuse_secret_key", "keycloak_client_secret"]:
        if k in masked:
            masked[k] = "***"
    return masked


def reload_config() -> Dict[str, Any]:
    """Reload config from disk."""
    return load_config()

# Initial load
load_config()
