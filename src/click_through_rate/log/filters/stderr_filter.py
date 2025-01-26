import logging


class StderrFilter(logging.Filter):
    """A custom logging filter that filters log records based on their level.

    This filter allows log records with a level greater than logging.INFO to pass through.
    """

    def filter(self, record: logging.LogRecord) -> bool | logging.LogRecord:
        return record.levelno > logging.INFO
