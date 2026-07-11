import logging
import os
from logging import Filter
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()


class RelativePathFilter(Filter):

    def filter(self, record):
        abs_path = Path(record.abspath).resolve()
        try:
            rel_path = abs_path.relative_to(PROJECT_ROOT)
        except Exception as ex:
            rel_path = abs_path.name
        record.rel_path = rel_path
        return True


class AppLogger:

    def __init__(self, name):
        pass

    def get_logger(self):
        pass
