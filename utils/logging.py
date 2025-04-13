import logging
import typing as t


def get_logger(name: t.Optional[str] = None) -> logging.Logger:
    """
    Get the logger instance for the application.

    Returns:
        Logger: The logger instance.
    """
    logger = logging.getLogger(name)
    return logger
