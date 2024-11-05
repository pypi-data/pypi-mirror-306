import logging
import sys
import typing as tp
from pathlib import Path


def init_logger(*, name: str, path: tp.Optional[Path], level=logging.DEBUG, log_format: str = "%(message)s") -> None:
    logger = logging.getLogger(name)
    logger.setLevel(level=level)

    formatter = logging.Formatter(log_format)

    if path is None:
        handler = logging.StreamHandler(stream=sys.stdout)
    else:
        path.parent.mkdir(exist_ok=True, parents=True)
        path.touch(exist_ok=True)
        handler = logging.FileHandler(path, mode="w+")

    handler.setFormatter(formatter)
    logger.addHandler(handler)
