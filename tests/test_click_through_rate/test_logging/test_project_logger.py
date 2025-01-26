import logging

from click_through_rate.log.project_logger import ProjectLogger


class TestProjectLogger:
    def test_create_logger(self):
        logger = ProjectLogger()
        logger.create_logger()

        assert logger._logger is not None  # pylint: disable=protected-access

    def test_create_log_message(self):
        logger = ProjectLogger()
        logger.create_logger()
        message = "This is a test message"
        log_message = logger.create_log_message(method=logger.create_log_message, message=message)

        assert log_message == f"ProjectLogger.ProjectLogger.create_log_message: {message}"

    def test_log_debug(self, caplog):
        caplog.set_level(logging.DEBUG)

        logger = ProjectLogger()
        logger.create_logger()
        message = "This is a test message"
        logger.log_debug(logger.log_debug, message)

        assert f"ProjectLogger.ProjectLogger.log_debug: {message}" in caplog.text

    def test_log_info(self, caplog):
        caplog.set_level(logging.INFO)

        logger = ProjectLogger()
        logger.create_logger()
        message = "This is a test message"
        logger.log_info(logger.log_info, message)

        assert f"ProjectLogger.ProjectLogger.log_info: {message}" in caplog.text

    def test_log_warning(self, caplog):
        caplog.set_level(logging.WARNING)

        logger = ProjectLogger()
        logger.create_logger()
        message = "This is a test message"
        logger.log_warning(logger.log_warning, message)

        assert f"ProjectLogger.ProjectLogger.log_warning: {message}" in caplog.text

    def test_log_error(self, caplog):
        caplog.set_level(logging.ERROR)

        logger = ProjectLogger()
        logger.create_logger()
        message = "This is a test message"

        try:
            raise ValueError("This is a test error")
        except ValueError as error:
            logger.log_error(logger.log_error, message, extra={"error": error})

        assert f"ProjectLogger.ProjectLogger.log_error: {message}" in caplog.text
        assert "ValueError: This is a test error" in caplog.text

    def test_log_critical(self, caplog):
        caplog.set_level(logging.CRITICAL)

        logger = ProjectLogger()
        logger.create_logger()
        message = "This is a test message"
        logger.log_critical(logger.log_critical, message)

        assert f"ProjectLogger.ProjectLogger.log_critical: {message}" in caplog.text
