import logging
import random
import string
import typing as tp
from pathlib import Path


class MetricLogger:
    def __init__(self, path: tp.Union[Path, str]):
        self.path = path if isinstance(path, Path) else Path(path)
        self.logger_name = ''.join(random.choices(string.ascii_lowercase, k=32))
        self.columns: tp.Optional[tp.List[str]] = None
        self.create_logger()

    def create_logger(self):
        logger = logging.getLogger(self.logger_name)

        # Create parent folders of self.path
        self.path.parent.mkdir(exist_ok=True, parents=True)
        self.path.touch(exist_ok=True)

        handler = logging.FileHandler(self.path, mode="w+")
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
        logger.setLevel(level=logging.DEBUG)

    def add(self, data: tp.Dict[str, float]):
        if self.columns is None:
            self.columns = list(data.keys())
            self.log(self.columns)

        self.log([data.get(column, None) for column in self.columns])

    def log(self, args: tp.List) -> None:
        logger = logging.getLogger(self.logger_name)
        frm = ",".join(["{}"] * len(args))
        logger.log(logging.CRITICAL, msg=frm.format(*args))
