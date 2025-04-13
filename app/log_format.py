import sys
import logging
import colorlog


def configure_log_format() -> None:
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s:%(reset)s %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bold",
        },
        reset=True,
        style="%",
    )
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[stream_handler])
