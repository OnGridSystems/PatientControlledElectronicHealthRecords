import logging


class LoggerMixin:
    _logger = None

    def _init_logger(self):
        name = '%s.%s' % (
            self.__class__.__module__,
            self.__class__.__name__
        )

        self._logger = logging.getLogger(name)

    @property
    def logger(self):
        if self._logger is None:
            self._init_logger()

        return self._logger
