import sys
from logging import Logger


class SDKLogger:
    def __init__(self):
        self._logger = None

    def set_logger(self, logger: Logger):
        self._logger = logger

    def debug(self, message):
        if self._logger:
            self._logger.debug(message)

    def info(self, message):
        if self._logger:
            self._logger.info(message)
        else:
            print(message)

    def warn(self, message):
        if self._logger:
            self._logger.warning(message)
        else:
            print(message)

    def error(self, message):
        if self._logger:
            self._logger.error(message)
        else:
            print(message, file=sys.stderr)


# Create a singleton instance
_global_logger = SDKLogger()
