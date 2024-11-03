import logging
import os
import sys
import warnings
from typing import Optional


def get_log_level_from_env(default: int = logging.INFO) -> int:
    """
    Get log level from BBSKY_LOG_LEVEL environment variable if it exists.
    Valid values are: DEBUG, INFO, WARNING, ERROR, CRITICAL
    """
    level_str = os.environ.get("BBSKY_LOG_LEVEL", "").upper()

    if level_str:
        try:
            return getattr(logging, level_str)
        except AttributeError:
            warnings.warn(f"Warning: Invalid log level '{level_str}'. Using default.")

    return default


def setup_logger(name: str = "bbsky", level: Optional[int] = None) -> logging.Logger:
    """
    Create and configure a logger that can be used throughout the library.

    Args:
        name (str): The name of the logger (default: "bbsky")
        level (int): The logging level (default: None, will use BBSKY_LOG_LEVEL env var or INFO)
    """
    # Use provided level, or get from env, or fall back to INFO
    level = level or get_log_level_from_env()

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level=level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )

        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


# Create a default logger instance
logger = setup_logger()
