import logging

import pytest


@pytest.fixture
def log_record_info() -> logging.LogRecord:
    return logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="/path/to/file.py",
        lineno=10,
        msg="Test message",
        args=None,
        exc_info=None,
    )


@pytest.fixture
def log_record_warning() -> logging.LogRecord:
    return logging.LogRecord(
        name="test_logger",
        level=logging.WARNING,
        pathname="/path/to/file.py",
        lineno=10,
        msg="Test message",
        args=None,
        exc_info=None,
    )
