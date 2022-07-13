from loguru import logger
from pathlib import Path

__log_path = Path("logs/file.log")
logger.add(__log_path.absolute(), rotation="50MB")

zlogger = logger
