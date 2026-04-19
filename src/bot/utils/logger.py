import logging
import os

from src.bot.core.config import LOGS_PATH


class Logger:
    def __init__(self, name: str) -> None:
        self.logger = logging.getLogger(name)
        self.setup_logger()

    def setup_logger(self) -> None:
        self.logger.setLevel(logging.INFO)

        stream = logging.StreamHandler()

        if not os.path.exists(LOGS_PATH):
            os.mkdir(LOGS_PATH)

        file = logging.FileHandler(LOGS_PATH + self.logger.name)

        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        stream.setFormatter(formatter)
        file.setFormatter(formatter)

        self.logger.addHandler(stream)
        self.logger.addHandler(file)

    def get_logger(self) -> logging.Logger:
        return self.logger
