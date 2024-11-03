from typing import Optional
import logging

try:
    from rich.logging import RichHandler

    _format = "%(message)s"
    _datefmt = None
    _handlers = [
        RichHandler(
            show_level=True,
            show_path=False,
            log_time_format="%H:%M:%S",
            omit_repeated_times=False,
        )
    ]
except ImportError:
    _format = "%(asctime)s  %(levelname)s    %(message)s"
    _datefmt = "%H:%M:%S"
    _handlers = None

__all__ = [
    "getLogger",
]


def getLogger(name: Optional[str] = None) -> logging.Logger:
    logging.basicConfig(
        format=_format,
        datefmt=_datefmt,
        level=logging.INFO,
        handlers=_handlers,
    )
    return logging.getLogger(name)
