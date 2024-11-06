import logging
import typing as tp


class MetricLogger:
    def __init__(self, logger_name: str):
        self.logger_name = logger_name
        self.columns: tp.Optional[tp.List[str]] = None

    def add(self, data: tp.Dict[str, float]):
        if self.columns is None:
            self.columns = list(data.keys())
            self.log(self.columns)

        self.log([data.get(column, None) for column in self.columns])

    def log(self, args: tp.List) -> None:
        logger = logging.getLogger(self.logger_name)
        frm = ",".join(["{}"] * len(args))
        logger.log(logging.CRITICAL, msg=frm.format(*args))
