"""Central logging."""

import logging


class Logger:

    def __init__(self):
        self._logger = logging.getLogger("AIPlatform")

        if not self._logger.handlers:

            handler = logging.StreamHandler()

            formatter = logging.Formatter(
                "[%(levelname)s] %(asctime)s | %(message)s"
            )

            handler.setFormatter(formatter)

            self._logger.addHandler(handler)

            self._logger.setLevel(logging.INFO)

    def info(self, message: str):
        self._logger.info(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def error(self, message: str):
        self._logger.error(message)

    def debug(self, message: str):
        self._logger.debug(message)


logger = Logger()
