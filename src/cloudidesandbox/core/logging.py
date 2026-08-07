import logging
import os
from logging import Filter
from pathlib import Path
from typing import Literal

PROJECT_ROOT = Path(__file__).parents[1].resolve()


class RelativePathFilter(Filter):

    def filter(self, record):
        abs_path = Path(record.pathname).resolve()
        try:
            rel_path = abs_path.relative_to(PROJECT_ROOT)
        except Exception as ex:
            rel_path = abs_path.name
        record.relpath = rel_path
        return True


class AppLogger:

    def __init__(
        self,
        name: str,
        *,
        log_file="logs/app.log",
        to_console: bool = True,
        to_file: bool = False,
        log_format: str = "%(asctime)s [%(levelname)s] {%(relpath)s}: %(message)s",
        logging_level: Literal[
            "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
        ] = "INFO",
    ):
        self.logger = logging.getLogger(name)
        log_lvl = self.get_level(logging_level)
        log_fmt = logging.Formatter(log_format)
        path_filter = RelativePathFilter()
        handlers = []
        self.logger.setLevel(log_lvl)
        if to_console:
            console_handler = logging.StreamHandler()
            handlers.append(console_handler)
        if to_file:
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            handlers.append(file_handler)
        for handler in handlers:
            handler.setLevel(log_lvl)
            handler.addFilter(path_filter)
            handler.setFormatter(log_fmt)
            self.logger.addHandler(handler)

    def get_level(self, level: str):
        match (level):
            case "DEBUG", _:
                return logging.DEBUG
            case "INFO":
                return logging.INFO
            case "WARNING":
                return logging.WARNING
            case "ERROR":
                return logging.ERROR
            case "CRITICAL":
                return logging.CRITICAL
            case _:
                return logging.INFO

    def get_logger(self):
        return self.logger
