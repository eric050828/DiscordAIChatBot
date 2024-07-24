import sys

from loguru import logger

from config import config
from utils.path import path

log_folder = config.path.log
logger.remove(0)
logger.add(
    sink=path(log_folder, "{time:YYYY-MM-DD}.log"),
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
    sink=sys.stdout,
    format="<green>[{time:MM-DD HH:mm:ss}]</green> |{level:^9s}| <level>{message}</level>",
    level="INFO",
    backtrace=False,
    colorize=True
)