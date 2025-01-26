import datetime as dt
import json
import logging

LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


class JSONFormatter(logging.Formatter):
    """A custom logging formatter that formats log records as JSON.

    Args:
        fmt_keys (dict[str, str] | None): A dictionary mapping log record attributes to their desired JSON keys.
            If None, no additional formatting will be applied. Defaults to None.

    Methods:
        format(record: logging.LogRecord) -> str:
            Formats the log record as a JSON string.

    Attributes:
        fmt_keys (dict[str, str]): A dictionary mapping log record attributes to their desired JSON keys.

    """

    def __init__(
        self,
        *,
        fmt_keys: dict[str, str] | None = None,
    ):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record as a JSON string.

        Args:
            record (logging.LogRecord): The log record to be formatted.

        Returns:
            str: The log record formatted as a JSON string.

        """
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord):
        """Prepares the log record dictionary for formatting as JSON.

        Args:
            record (logging.LogRecord): The log record to be prepared.

        Returns:
            dict: The prepared log record dictionary.

        """
        permanent_fields = {
            "message": record.getMessage(),
            "timestamp": dt.datetime.fromtimestamp(record.created, tz=dt.UTC).isoformat(),
        }

        if record.exc_info is not None:
            permanent_fields["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            permanent_fields["stack_info"] = self.formatStack(record.stack_info)

        message = {
            key: (permanent_fields.pop(value) if value in permanent_fields else getattr(record, value))
            for key, value in self.fmt_keys.items()
        }
        message.update(permanent_fields)
        message.update({key: value for key, value in record.__dict__.items() if key not in LOG_RECORD_BUILTIN_ATTRS})

        return message
