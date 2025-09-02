"""Loguru rotating log setup."""
from loguru import logger
import os

LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

os.makedirs(LOG_DIR, exist_ok=True)
logger.remove()
logger.add(LOG_FILE, rotation="10 MB", retention="10 days", enqueue=True, backtrace=True, diagnose=True)
logger.add(lambda msg: print(msg, end=""), level="INFO")
