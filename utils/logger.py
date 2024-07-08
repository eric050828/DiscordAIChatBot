from datetime import datetime

from loguru import logger

from .config import get_config


log_folder = get_config("logger", "folder")

logger.add(
    sink=f"{log_folder}/{{time:YYYY-MM-DD}}.log",
    format="{time:MM-DD HH:mm:ss} {level} {message}",
    level="INFO",
    serialize=True,
    backtrace=False,
    diagnose=False,
    enqueue=True,
    rotation="00:00",
    retention="1 month",
    compression="zip",
    encoding="utf-8",
)

logger.add(
    sink=lambda message: "<green>{message.time:MM-DD HH:mm:ss}</green> <level>{message}<level>",
    colorize=True,
)