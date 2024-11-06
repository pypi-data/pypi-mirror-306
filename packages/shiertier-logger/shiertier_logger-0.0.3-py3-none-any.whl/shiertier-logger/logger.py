import os.path
from os import makedirs
from loguru import logger
import sys
from typing import Dict, Any

__all__ = ["logger", "Logger_I18n", "easy_logger_i18n"]

LOG_DIR = os.environ.get("LOG_DIR", "logs")
if not LOG_DIR:
    LOG_DIR = os.path.join(os.path.expanduser("~"), ".shiertier", "logs")
makedirs(LOG_DIR, exist_ok=True)
log_file_path = os.path.join(LOG_DIR, "file_{time}.log")

LOG_LEVEL_STR = os.environ.get("LOG_LEVEL", "INFO")
LOG_SYS_BOOL = os.environ.get("LOG_SYS", "True").lower() in ["1", "true"]

logger.remove()
logger.add(log_file_path, rotation="1 MB", level=LOG_LEVEL_STR)  # 1MB for each file

if LOG_SYS_BOOL:
    logger.add(sys.stdout, level=LOG_LEVEL_STR)

try:
    from shiertier_i18n import i18n
except ImportError:
    logger.warning("shiertier_i18n not found, can't use translation support")
    def i18n(message: str, replace_dict: Dict[str, Any] = None) -> str:
        for key, value in replace_dict.items():
            message = message.replace(key, value)
        return message

class Logger_I18n:
    def __init__(self, base_logger, i18n_func):
        self.base_logger = base_logger
        self.i18n_func = i18n_func

    def info(self, message: str, replace_dict: Dict[str, Any] = None) -> None:
        """Logs an info message with translation support."""
        translated_message = self.i18n_func(message, replace_dict)
        self.base_logger.info(translated_message)

    def debug(self, message: str, replace_dict: Dict[str, Any] = None) -> None:
        """Logs a debug message with translation support."""
        translated_message = self.i18n_func(message, replace_dict)
        self.base_logger.debug(translated_message)

    def warning(self, message: str, replace_dict: Dict[str, Any] = None) -> None:
        """Logs a warning message with translation support."""
        translated_message = self.i18n_func(message, replace_dict)
        self.base_logger.warning(translated_message)

    def error(self, message: str, replace_dict: Dict[str, Any] = None) -> None:
        """Logs an error message with translation support."""
        translated_message = self.i18n_func(message, replace_dict)
        self.base_logger.error(translated_message)

easy_logger_i18n = Logger_I18n(logger, i18n)