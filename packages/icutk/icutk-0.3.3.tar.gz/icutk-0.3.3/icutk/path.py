from typing import Union
from pathlib import Path
import os

__all__ = [
    "abspath",
    "realpath",
    "expandpath",
]


def abspath(path: Union[str, Path]) -> Path:
    return Path(path).absolute()


def realpath(path: Union[str, Path]) -> Path:
    return Path(path).resolve()


def expandpath(path: Union[str, Path]) -> Path:
    return Path(os.path.expanduser(os.path.expandvars(str(path))))
