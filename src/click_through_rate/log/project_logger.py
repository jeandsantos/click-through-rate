"""Logger for the project."""

import logging
from collections.abc import Callable

from click_through_rate.log.logging_configs import LOG_MESSAGE_TEMPLATE


class ProjectLogger:
    """Logger for the project."""

    _logger: logging.Logger

    def create_logger(self) -> None:
        self._logger: logging.Logger = logging.getLogger(self.__class__.__qualname__)
        self.log_info(method=self.create_logger, message="Logger created.")

    def create_log_message(self, method: Callable, message: str) -> str:
        """Create a log message.

        Args:
            method (Callable): The function that is logging the message.
            message (str): The message to be logged.

        Returns:
            str: The log message.

        """
        return LOG_MESSAGE_TEMPLATE.format(
            class_name=self.__class__.__qualname__,
            function_name=method.__qualname__,
            message=message,
        )

    def log_debug(self, method: Callable, message: str, extra: dict[str, str] | None = None) -> None:
        """Log a debug message.

        Args:
            method (Callable): The function that is logging the message.
            message (str): The message to be logged.
            extra (dict[str, str] | None): Additional context to be logged. Defaults to None.

        """
        message = self.create_log_message(method=method, message=message)
        self._logger.debug(message, extra=extra)

    def log_info(self, method: Callable, message: str, extra: dict[str, str] | None = None) -> None:
        """Log a info message.

        Args:
            method (Callable): The function that is logging the message.
            message (str): The message to be logged.
            extra (dict[str, str] | None): Additional context to be logged. Defaults to None.

        """
        message = self.create_log_message(method=method, message=message)
        self._logger.info(message, extra=extra)

    def log_warning(self, method: Callable, message: str, extra: dict[str, str] | None = None) -> None:
        """Log a warning message.

        Args:
            method (Callable): The function that is logging the message.
            message (str): The message to be logged.
            extra (dict[str, str] | None): Additional context to be logged. Defaults to None.

        """
        message = self.create_log_message(method=method, message=message)
        self._logger.warning(message, extra=extra)

    def log_error(self, method: Callable, message: str, extra: dict[str, str] | None = None) -> None:
        """Log a error message.

        Args:
            method (Callable): The function that is logging the message.
            message (str): The message to be logged.
            extra (dict[str, str] | None): Additional context to be logged. Defaults to None.

        """
        message = self.create_log_message(method=method, message=message)
        self._logger.error(message, extra=extra, exc_info=True)

    def log_critical(self, method: Callable, message: str, extra: dict[str, str] | None = None) -> None:
        """Log a critical message.

        Args:
            method (Callable): The function that is logging the message.
            message (str): The message to be logged.
            extra (dict[str, str] | None): Additional context to be logged. Defaults to None.

        """
        message = self.create_log_message(method=method, message=message)
        self._logger.critical(message, extra=extra)
